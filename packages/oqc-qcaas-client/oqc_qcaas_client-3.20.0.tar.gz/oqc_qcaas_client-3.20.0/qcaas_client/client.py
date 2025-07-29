# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Oxford Quantum Circuits Ltd
import json
import logging
import re
import textwrap
import threading
import warnings
from collections import defaultdict
from datetime import datetime
from enum import Enum
from functools import wraps
from importlib.metadata import version
from json import JSONDecodeError
from time import sleep
from typing import Dict, List, Optional, Union
from urllib.parse import quote, urlparse
from uuid import uuid4

import requests
from compiler_config.config import CompilerConfig, QuantumResultsFormat
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def format_warning(msg):
    return "\n".join(
        [
            "",
            "",
            "*" * 35 + " WARNING! " + "*" * 35,
            textwrap.fill(msg, 80),
            "*" * 80,
            "",
        ]
    )


class TaskStatus(Enum):
    # Keep in sync with qcaas
    UNKNOWN = "UNKNOWN"
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class ServerException(Exception):
    """Generic exception thrown back from the server."""

    def __init__(self, message, server_error_code, metadata=None):
        super().__init__(message)
        self.server_error_code = server_error_code
        self.metadata = metadata or dict()


class ConnectionFailureException(ServerException):
    def __init__(self, status_code):
        self.status_code = status_code
        code = ""
        retry_status_codes = [408, 409, 429, 500, 502, 503, 504]
        if status_code in retry_status_codes:
            code = " code"
        super().__init__(
            f"The client is experiencing issues communicating with the QCaaS at present. Please try again later. Error{code}: {status_code}",
            status_code,
            {},
        )


class ExperimentalConfig(CompilerConfig):
    """
    Wrapper for existing CompilerConfig which adds external backend specific parameters
    (e.g. bond dim, noise, noise model). Config validation then occurs at the correct
    submission service for that backend.
    """

    def __init__(
        self,
        *,
        noise: bool = False,
        bond_dimension: Optional[int] = None,
        noise_model=None,
        **compiler_kwargs,
    ):
        super().__init__(**compiler_kwargs)
        self.noise = noise
        self.bond_dimension = bond_dimension
        if noise_model is not None:
            # conditional import if noise model provided
            try:
                from qcshared.json.encode import jsonify
                from qcshared.noise_models.model import NoiseModel
            except ModuleNotFoundError as e:
                raise ImportError(
                    "ExperimentalConfig needs the 'experimental' extra:\n"
                    "    pip install oqc-qcaas-client[experimental]"
                ) from e
            if not isinstance(noise_model, (dict, NoiseModel)):
                raise TypeError("Noise model must be a NoiseModel or dict.")

            self.noise_model = (
                jsonify(noise_model)
                if isinstance(noise_model, NoiseModel)
                else noise_model
            )
        else:
            self.noise_model = None

    def _external_config(self) -> Dict:
        ext: Dict = {}
        if self.noise:
            ext["noise_enabled"] = True
        if self.bond_dimension is not None:
            ext["bond_dimension"] = self.bond_dimension
        if self.noise_model is not None:
            ext["noise_model"] = self.noise_model
        return ext

    def to_json(self) -> str:
        """Overrides CompilerConfig to_json() to include serialisation of external config"""
        base = json.loads(super().to_json())
        for k in ("noise", "bond_dimension", "noise_model"):
            base.get("$data").pop(k, None)
        ext = self._external_config()
        if ext:
            base["$external"] = ext
        return json.dumps(base)

    @classmethod
    def create_from_json(cls, serialized: str):
        data = json.loads(serialized)
        ext = data.pop("$external", {})
        noise = ext.get("noise_enabled", False)
        bond_dimension = ext.get("bond_dimension", None)
        noise_model = ext.get("noise_model", None)
        base = CompilerConfig.create_from_json(json.dumps(data))
        return cls(
            noise=noise,
            bond_dimension=bond_dimension,
            noise_model=noise_model,
            **base.__dict__,
        )

    @property
    def external_config(self) -> Dict:
        return self._external_config()

    @property
    def base_config(self) -> CompilerConfig:
        return CompilerConfig.create_from_json(super().to_json())


class QPUTask:
    """
    Payload for executing tasks on a QPU. Program is the QASM program to be executed.
    """

    def __init__(
        self,
        program: str,
        config: Optional[Union[CompilerConfig, ExperimentalConfig]] = None,
        task_id=None,
        hybrid_marker=None,
        qpu_id=None,
        tag="",
    ):
        self.task_id = task_id
        self.program = program
        self.config = (
            config.base_config if isinstance(config, ExperimentalConfig) else config
        )
        self.hybrid_marker: Optional[str] = hybrid_marker
        self.qpu_id: Optional[str] = qpu_id
        self.tag: Optional[str] = tag
        self.external_config: Dict = (
            config.external_config if isinstance(config, ExperimentalConfig) else {}
        )

        if not self.config:
            self.config = CompilerConfig(
                results_format=QuantumResultsFormat().binary_count()
            )

    def to_json(self, omit_empty_task_id=False):
        task = {
            "program": self.program,
            "config": self.config.to_json(),
            "qpu_id": self.qpu_id,
            "tag": self.tag,
        }
        if self.hybrid_marker:
            task["hybrid_marker"] = self.hybrid_marker
        if self.external_config:
            task["external_config"] = self.external_config
        # Allows single tasks without a task_id to be
        # submitted in a single REST API call in schedule_task.
        if self.task_id:
            task["task_id"] = self.task_id
        elif not omit_empty_task_id:
            task["task_id"] = -1
        return task

    def __str__(self):
        return f"QPUTask [id={self.task_id}, qpu={self.qpu_id}]"


class QPUTaskResult:
    def __init__(self, id_, result=None, metrics=None, error_details=None):
        self.id = id_
        self.result = result
        self.metrics = metrics or dict()
        self.error_details: QPUTaskErrors = error_details

    def has_errored(self):
        return self.error_details is not None


class QPUTaskErrors:
    def __init__(self, error_message, error_code=None):
        self.error_code = error_code or -1
        self.error_message = error_message


def _get_unscheduled_tasks_results(tasks, scheduled_tasks) -> list[str]:
    results = []
    unscheduled_tasks = [task for task in tasks if task not in scheduled_tasks]
    for task in unscheduled_tasks:
        results.append(
            QPUTaskResult(
                id_=task.task_id,
                error_details=QPUTaskErrors("Failed to schedule task."),
            )
        )
    return results


class OQCClient:
    def __init__(
        self,
        url,
        email=None,
        password=None,
        timeout=(10, 30),
        authentication_token=None,
    ):
        self.server_version = None
        self._authentication_token = authentication_token
        self._qpus = None
        self.timeout = timeout
        self.session = requests.Session()
        self.default_qpu_id = "qpu:uk:3:9829a5504f"
        self.is_client_initialized = True
        if email:
            self._email = _validated_email(email)
        else:
            self._email = None
        if password:
            self._password = _validated_password(password)
        else:
            self._password = None

        if url is None:
            raise ValueError("Need a URL to connect too.")

        if (email and not password) or (password and not email):
            raise ValueError(
                "If one of email and password are provided, both must be provided"
            )

        if authentication_token and (email or password):
            raise ValueError(
                "If one authentication_token is specified, "
                "email and password must not be specified"
            )

        adapter = HTTPAdapter(
            max_retries=Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[408, 409, 429, 500, 502, 503, 504],
                allowed_methods=frozenset({"DELETE", "GET", "PUT"}),
            )
        )

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # build the user agent
        ver = ""
        try:
            ver = version("oqc-qcaas-client")
        except Exception as e:
            warnings.warn(f"Unable to get the client version, with exception {e}")
        self.user_agent_string = "QCaaS Client " + ver

        self.server_lock = threading.Lock()

        # get the server version
        self.url = _validated_url(url)
        try:
            server_version = self._get("/admin/version", authenticate=False).json()
        except Exception as e:
            logging.error(f"Exception: {e}")
            t = f"OQC Client failed to initialize with url {url}, please check your access and the server status"
            logging.error(format_warning(t))
            self.is_client_initialized = False
            return
        try:
            self.server_version = server_version["version"]
        except Exception as e:
            logging.error(f"Exception: {e}")
            t = "OQC Client failed to initialize due to an incorrect server version, please check your access and the server status"
            logging.error(format_warning(t))
            self.is_client_initialized = False
            return
        all_active_qpus = self.get_qpus()
        if all_active_qpus == []:
            t = "OQC Client failed to initialize as no active Qpus are available, please check your access and the server status"
            logging.error(format_warning(t))
            self.is_client_initialized = False

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = _validated_email(value)
        self._authentication_token = None  # Clear existing token to force re-auth.

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = _validated_password(value)
        self._authentication_token = None  # Clear existing token to force re-auth.

    def client_initialized_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.is_client_initialized:
                t = "This method can't be called as the OQC client failed to initialize"
                logging.error(format_warning(t))
                return None
            return func(self, *args, **kwargs)

        return wrapper

    def default_qpu_id_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            default_qpu_used_warning = "No QPU ID was provided, so default QPU ID was used. However, this functionality will soon be depracated and not providing a QPU ID will cause an error."
            if args:
                first_arg = args[0]

                # Case 1: first_arg is None
                if first_arg is None or first_arg == []:
                    logging.critical(format_warning(default_qpu_used_warning))

                # Case 2: first_arg is a list
                elif isinstance(first_arg, list):
                    for key in kwargs.keys():
                        if key == "qpu_id":
                            return func(self, *args, **kwargs)
                    for item in first_arg:
                        if (
                            hasattr(item, "qpu_id")
                            and getattr(item, "qpu_id", None) is None
                        ):
                            logging.critical(format_warning(default_qpu_used_warning))
                            break

                # Case 3: first_arg is a single object with qpu_id
                elif hasattr(first_arg, "qpu_id"):
                    if getattr(first_arg, "qpu_id", None) is None:
                        logging.critical(format_warning(default_qpu_used_warning))
                    elif len(args) > 1:
                        if args[1] is None:
                            logging.critical(format_warning(default_qpu_used_warning))

            return func(self, *args, **kwargs)

        return wrapper

    def _handle_response_error(self, response):
        retry_status_codes = [408, 409, 429, 500, 502, 503, 504]
        if response.status_code in retry_status_codes:
            raise ConnectionFailureException(response.status_code)
        elif response.status_code != 200:
            raise ServerException(
                response.content.decode("utf-8"), response.status_code
            )
        if response.status_code == 401:
            raise ServerException("Authentication Error", response.status_code, {})

        if response.status_code != 200:
            # Right now we can, occasionally, return HTML blobs. Looks ugly,
            # but better than parsing exception.
            if not response.headers.get("content-type", "").startswith(
                "application/json"
            ):
                raise ServerException(
                    response.content.decode("utf-8"), response.status_code
                )
            else:
                exception_info = response.json()
                if "response" in exception_info:
                    raise ServerException(
                        exception_info["response"]["errors"][0],
                        response.status_code,
                        exception_info,
                    )

    def _handle_response_messages(self, response):
        try:
            response = response.json()
            if isinstance(response, dict):
                messages = [response.get("message", "")]
                messages.extend(response.get("messages", []))
                for message in messages:
                    if message != "":
                        if message.startswith("Warning"):
                            warnings.warn(message)
                        else:
                            logging.info(message)
        except JSONDecodeError:
            pass

    def _put(self, endpoint, data=None, authenticate=True, json=None, **kwargs):
        """Helper for put requests. Applies common info such as headers etc."""

        if authenticate:
            self.authenticate()
        headers = kwargs.get("headers", self._build_headers(json_content=True))
        if not endpoint.startswith("http"):
            endpoint = self.url + endpoint
        try:
            response = self.session.put(
                endpoint,
                data,
                json=json,
                headers=headers,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.Timeout:
            raise ConnectionFailureException("Timeout error")
        self._handle_response_error(response)
        self._handle_response_messages(response)
        return response

    def _get(
        self, endpoint, params=None, data=None, json=None, authenticate=True, **kwargs
    ):
        """Helper for get requests. Applies common info such as headers etc."""

        if authenticate:
            self.authenticate()
        headers = kwargs.get("headers", self._build_headers())
        if not endpoint.startswith("http"):
            endpoint = self.url + endpoint
        try:
            response = self.session.get(
                endpoint,
                params=params,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.Timeout:
            raise ConnectionFailureException("Timeout error")
        self._handle_response_error(response)
        self._handle_response_messages(response)
        return response

    def _post(self, endpoint, json=None, data=None, authenticate=True, **kwargs):
        """Helper for post requests. Applies common info such as headers etc."""

        if authenticate:
            self.authenticate()
        auth_headers = self._build_headers()
        headers = kwargs.pop("headers") if kwargs.get("headers") is not None else {}
        if not endpoint.startswith("http"):
            endpoint = self.url + endpoint
        try:
            response = self.session.post(
                endpoint,
                data,
                json,
                headers=headers | auth_headers,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.Timeout:
            raise ConnectionFailureException("Timeout error")
        self._handle_response_error(response)
        self._handle_response_messages(response)
        return response

    def _delete(self, endpoint, json=None, data=None, authenticate=True, **kwargs):
        """Helper for post requests. Applies common info such as headers etc."""

        if authenticate:
            self.authenticate()
        auth_headers = self._build_headers()
        headers = kwargs.pop("headers") if kwargs.get("headers") is not None else {}
        if not endpoint.startswith("http"):
            endpoint = self.url + endpoint
        try:
            response = self.session.delete(
                endpoint,
                data,
                json,
                headers=headers | auth_headers,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.Timeout:
            raise ConnectionFailureException("Timeout error")
        self._handle_response_error(response)
        self._handle_response_messages(response)
        return response

    def authenticate(self):
        if self._authentication_token is not None:
            return True
        if (
            self._email is None
            and self._password is None
            and self._authentication_token is None
        ):
            return False

        payload = {"email": self._email or "", "password": self._password or ""}
        self._post("/admin/logout", {}, authenticate=False)
        auth = self._post(
            "/admin/login?include_auth_token=true", payload, authenticate=False
        )
        response = auth.json()
        self._authentication_token = response["response"]["user"][
            "authentication_token"
        ]

        return self._authentication_token is not None

    @client_initialized_decorator
    def get_qpus(self):
        qpu_response = self._get("/admin/qpu").json()

        qpus = [q for q in qpu_response["items"] if q["active"]]
        if qpus == [] or qpus is None:
            t = "No active QPU is available for this client session, please try loging in again or check the server status"
            logging.error(format_warning(t))
            return []
        try:
            _ = next(
                qpu["id"]
                for qpu in qpus
                if qpu["id"] == self.default_qpu_id and qpu["active"]
            )
        except StopIteration:
            self.default_qpu_id = qpus[0]["id"]

        return qpus

    @default_qpu_id_decorator
    def _get_qpu_endpoint(self, qpu_id=None):
        if qpu_id is None or qpu_id == "" or qpu_id == "lucy":
            qpu_id = self.default_qpu_id
        if not self._qpus:
            self._qpus = self.get_qpus()

        try:
            url = next(qpu["url"] for qpu in self._qpus if qpu["id"] == qpu_id)
            return url
        except StopIteration:
            raise ValueError(f"Invalid qpu_id: {qpu_id}")

    def _build_headers(self, json_content=False):
        """Create authentication header."""
        headers = dict()
        headers["User-agent"] = self.user_agent_string
        if self._authentication_token is not None:
            headers["Authentication-Token"] = self._authentication_token

        if json_content:
            headers["Content-Type"] = "application/json"

        return headers

    @client_initialized_decorator
    def get_token_expiry_time(self) -> Optional[str]:
        if self._authentication_token is None:
            return None
        auth_token = self._get(
            f"/admin/auth_tokens/{self._authentication_token}"
        ).json()
        expires_at = auth_token["expires_at"]
        expires_time = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%S")
        base_date = datetime(1970, 1, 1)
        expires_timestamp = (expires_time - base_date).total_seconds()
        return int(expires_timestamp)

    @client_initialized_decorator
    def change_password(self, email, password, validate=True):
        """Change the users password"""
        user = self.get_user_info(email, validate)
        if user:
            response = self._post(
                f"/admin/users/{user['id']}/update_password",
                json={
                    "password": (
                        _validated_password(password) if validate else password
                    ),
                    "password_confirm": (
                        _validated_password(password) if validate else password
                    ),
                },
            )
        else:
            return None

        # If we're updating our own password, re-assign for re-auth.
        if response.status_code == 200 and self.email == email:
            self.password = password
        return response

    @client_initialized_decorator
    def get_password_expiry_time(self, email, validate=True) -> Optional[str]:
        user = self.get_user_info(email, validate)
        if user:
            results = self._get(f"/admin/users/{user['id']}").json()
        else:
            return None
        return results.get("password_expires_at", None)

    @client_initialized_decorator
    def get_user_info(self, email, validate=True):
        results = self._get(
            f"/admin/users?q={quote(_validated_email(email) if validate else email)}"
        ).json()

        if results["total"] > 0:
            return results["items"][0]
        else:
            return None

    @client_initialized_decorator
    def get_next_window(self, qpu_id=None) -> Optional[datetime]:
        """
        Fetches the next active window.
        """
        endpoint = self._get_qpu_endpoint(qpu_id)
        next_window_dict = self._get(endpoint + "/windows/next").json()

        if next_window_dict == {} or "next_window" not in next_window_dict:
            return None

        return _validate_datetime_format(
            next_window_dict.get("next_window").get("starting")
        )

    @client_initialized_decorator
    def create_one_off_window_(
        self,
        qpu_id,
        start_datetime,
        end_datetime,
        lease_type,
        lease_holder_name,
        duration_hours,
        window_name,
        window_start,
    ):
        params = {
            "qpu_id": qpu_id,
            "start_time": start_datetime,
            "end_time": end_datetime,
            "lease_type": lease_type,
            "lease_holder_name": lease_holder_name,
            "duration_hours": duration_hours,
            "window_name": window_name,
            "window_start": window_start,
        }

        return self._post("/windows/one-off-window", params)

    @client_initialized_decorator
    def get_dedicated_window_history(self, latest=False, qpu_id=None):
        params = {}
        if isinstance(latest, bool) and latest is True:
            params["latest"] = True

        endpoint = self._get_qpu_endpoint(qpu_id)

        return self._get(endpoint + "/windows/history", params).json()

    @client_initialized_decorator
    def password_reset(self, email, validate=True):
        """
        Sends an email to a user for them to reset a password.
        """
        self._post(
            "/password_reset",
            data={"email": _validated_email(email) if validate else email},
        )

    @client_initialized_decorator
    def create_auth_token(self, expires_at):
        """
        Create a new auth token.
        """
        try:
            datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("expires_at must be in the format 2024-12-31T23:59:59")

        token = self._post(
            "/admin/users/current_user/auth_tokens",
            json={"expires_at": expires_at},
        )
        self._handle_response_messages(token)
        response = token.json()
        return response["token"]

    @client_initialized_decorator
    def delete_auth_token(self, token):
        """
        Create a new auth token.
        """
        token = self._delete(f"/auth_tokens/{token}")
        self._handle_response_messages(token)
        response = token.json()
        return response["token"]

    @client_initialized_decorator
    def get_system_status(self, qpu_id=None):
        # FEATURE REQUEST: Result format may need expanding/making nicer.
        status_path = "/monitoring/statuses"
        if qpu_id:
            try:
                endpoint = self._get_qpu_endpoint(qpu_id)
            except ValueError:
                return []
            return self._get(endpoint + status_path).json()
        else:
            endpoints = list(set([qpu.endpoint for qpu in self._qpus]))
            if len(endpoints) == 1:
                return self._get(endpoints[0] + status_path).json()
            if len(endpoints) > 1:
                statuses = []
                for endpoint in endpoints:
                    status = self._get(endpoint + status_path).json()
                    statuses.append(status)
                return statuses
            else:
                logging.error("No QPUs available")
                return

    @default_qpu_id_decorator
    @client_initialized_decorator
    def get_calibration(self, qpu_id=None, date_filter=None):
        # FEATURE REQUEST: Find precise format of date filter,
        # align with types or parsing.
        if qpu_id is None or qpu_id == "lucy":
            qpu_id = self.default_qpu_id
        params = {"qpu_id": qpu_id}
        if date_filter is not None:
            params["date"] = str(date_filter)
        endpoint = self._get_qpu_endpoint(qpu_id)
        return self._get(endpoint + "/monitoring/calibrations", params).json()

    @default_qpu_id_decorator
    @client_initialized_decorator
    def get_features(self, qpu_id=None):
        if qpu_id is None or qpu_id == "lucy":
            qpu_id = self.default_qpu_id
        qpu_details = self._get(
            self.url + "/admin/qpu/" + qpu_id,
        ).json()
        return qpu_details["feature_set"]

    # Retry attempt = index of next attempted request delay.
    retry_cadence = [1, 2, 5, 8, 10, 15, 30]

    @client_initialized_decorator
    def execute_tasks(
        self,
        tasks: Union[QPUTask, List[QPUTask]],
        qpu_id: str = None,
        include_metrics=False,
    ) -> List[QPUTaskResult]:
        """
        Executes the QPU tasks and then blocks until a results are retrieved for all
        of them. Automatically disconnects socket unless auto_disconnect=False.
        """
        scheduled_tasks = self.schedule_tasks(tasks, qpu_id)

        def retry_delay(attempt):
            if attempt > len(self.retry_cadence):
                return self.retry_cadence[-1]

            if attempt <= 0:
                return self.retry_cadence[0]

            return self.retry_cadence[attempt - 1]

        # FEATURE REQUEST: Add processing timeout.
        results = []
        scheduled_count = len(scheduled_tasks)
        current_task_index = 0
        retry_attempt = 0
        while current_task_index < scheduled_count:
            scheduled_task = scheduled_tasks[current_task_index]
            try:
                task_info = self.get_task(scheduled_task.task_id, scheduled_task.qpu_id)
            except Exception as e:
                warnings.warn(f"Unable to execute a task, with exception {e}")
            status = self._get_task_status(task_info)
            if status == TaskStatus.FAILED.value:
                logging.info(f"{scheduled_task.task_id} failed execution.")
                error_details = self._get_task_errors(task_info)
                results.append(
                    QPUTaskResult(scheduled_task.task_id, error_details=error_details)
                )
            elif status == TaskStatus.COMPLETED.value:
                logging.info(f"{scheduled_task.task_id} completed execution.")
                qpu_result = self._get_task_results(scheduled_task.task_id, task_info)
                if include_metrics:
                    qpu_result.metrics = self.get_task_metrics(
                        scheduled_task.task_id, scheduled_task.qpu_id
                    )
                results.append(qpu_result)

            # If we have a new result, process the next block, otherwise
            # retry with increasing delay.
            if current_task_index != len(results):
                current_task_index = len(results)
                retry_attempt = 0
            else:
                logging.info(f"Still waiting on {scheduled_task.task_id}...")
                retry_attempt += 1
                sleep(retry_delay(retry_attempt))

        if not isinstance(tasks, list):
            tasks = [tasks]

        results.extend(_get_unscheduled_tasks_results(tasks, scheduled_tasks))

        return results

    @client_initialized_decorator
    def create_task_ids(
        self, ntasks: int, qpu_id: str = None, tag: str = None
    ) -> List[str]:
        server = self._get_qpu_endpoint(qpu_id)
        return self._post(
            f"{server}/tasks",
            json={"qpu_id": qpu_id, "task_count": ntasks, "tag": tag},
        ).json()

    @default_qpu_id_decorator
    @client_initialized_decorator
    def schedule_tasks(
        self, tasks: Union[QPUTask, List[QPUTask]], qpu_id: str = None, tag: str = None
    ) -> List[QPUTask]:
        """
        Schedules all tasks to run on the QPU and updates the task objects with the
        associated run ID's. Automatically disconnects socket unless
        auto_disconnect=False. If wait for acknowledgement the set of tasks returned
        will contain only those that are confirmed to have been scheduled, otherwise
        will just return all tasks.
        """

        if not isinstance(tasks, List):
            tasks = [tasks]

        invalid_tasks = [task for task in tasks if not isinstance(task, QPUTask)]
        if any(invalid_tasks):
            raise ValueError(
                f"{', '.join([str(task) for task in invalid_tasks])}"
                f" are invalid types to try and schedule."
            )

        # if qpu_id is provided, set it on all tasks
        if qpu_id:
            for task in tasks:
                task.qpu_id = qpu_id
        else:
            for task in tasks:
                if not task.qpu_id:
                    task.qpu_id = self.default_qpu_id

            # qpu_id is not provided globally, so it must be on all tasks already
            # and must be the same on all tasks
            qpu_id = tasks[0].qpu_id
            for task in tasks:
                if qpu_id != task.qpu_id:
                    raise ValueError("All tasks must have the same qpu_id")

        server = self._get_qpu_endpoint(qpu_id)
        endpoint = server + "/tasks/submit"

        if len(tasks) == 1 and tasks[0].task_id is None:
            # If there is a single task and it has no task_id, allow the submission service
            # to create task to avoid multiple REST API calls from the client to server
            # (see https://github.com/oqc-tech/qcaas/blob/8083b10a2cba994fb6d6882e429b64ede9d1a893/cloud/oqc_cloud/server/core/submission_service.py#L66-L73)
            if tag:
                tasks[0].tag = tag
            res = self._post(
                endpoint=endpoint,
                json={"tasks": [tasks[0].to_json(omit_empty_task_id=True)]},
            )
            tasks[0].task_id = res.json()[0]["task_id"]
            return tasks

        uninitialized_tasks = [t for t in tasks if t.task_id is None]
        if uninitialized_tasks:
            # If there are multiple tasks to be submitted, make a REST API call
            # to create a batch of tasks before submitting them
            task_ids = self.create_task_ids(len(uninitialized_tasks), qpu_id, tag)
            # Assign ID's to particular tasks. At this point the ID's have no
            # meaning beyond 'pending submission'.
            for task, task_id in zip(uninitialized_tasks, task_ids):
                task.task_id = task_id

        self._post(
            endpoint=endpoint,
            json={"tasks": [task.to_json() for task in tasks]},
        )
        return tasks

    def _get_task_results(self, task_id, task_info: dict):
        results = task_info.get("results", None)
        if results is None:
            return results

        return QPUTaskResult(task_id, results)

    @client_initialized_decorator
    def get_task_results(self, task_id, qpu_id: str = None) -> Optional[QPUTaskResult]:
        """
        Returns a QPUTaskResult that holds information about the tasks results
        and running. Returns none otherwise.
        """
        server = self._get_qpu_endpoint(qpu_id)
        endpoint = f"{server}/tasks/{str(task_id)}/results"

        results = self._get(endpoint).json()
        return self._get_task_results(task_id, results)

    def _get_task_errors(self, task_info: dict):
        error_details = task_info.get("task_error", None)
        if error_details is None:
            return None

        return QPUTaskErrors(
            error_details.get("error_message", "Unknown error."),
            error_details.get("error_code", -1),
        )

    @client_initialized_decorator
    def get_task_errors(self, task_id, qpu_id: str = None) -> Optional[QPUTaskErrors]:
        server = self._get_qpu_endpoint(qpu_id)
        endpoint = f"{server}/tasks/{str(task_id)}/error"
        errors = self._get(endpoint).json()
        return self._get_task_errors(errors)

    @client_initialized_decorator
    def get_tasks_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        qpu_id: str = None,
    ) -> list[dict]:
        server = self._get_qpu_endpoint(qpu_id)
        url = f"{server}/tasks"

        params = []
        if start_date is not None:
            params.append(f"start_date={start_date}")
        if end_date is not None:
            params.append(f"end_date={end_date}")

        url += f"?{'&'.join(params)}" if params else ""

        return self._get(url).json()

    def _get_task_status(self, task_info: dict):
        return task_info.get("status", TaskStatus.UNKNOWN.value)

    @client_initialized_decorator
    def get_task_status(self, task_id, qpu_id: str = None):
        server = self._get_qpu_endpoint(qpu_id)
        endpoint = f"{server}/tasks/{str(task_id)}/status"

        status = self._get(endpoint).json()
        return self._get_task_status(status)

    @client_initialized_decorator
    def get_task(self, task_id, qpu_id: str = None):
        server = self._get_qpu_endpoint(qpu_id)
        endpoint = f"{server}/tasks/{str(task_id)}/all_info"
        return self._get(endpoint).json()

    def _get_task_metrics(self, task_info: dict):
        return task_info.get("execution_metadata", None)

    @client_initialized_decorator
    def get_task_metrics(self, task_id, qpu_id: str = None):
        server = self._get_qpu_endpoint(qpu_id)
        endpoint = f"{server}/tasks/{str(task_id)}/execution_metadata"
        metrics = self._get(endpoint).json()
        return self._get_task_metrics(metrics)

    def _get_task_metadata(self, task_info: dict):
        return task_info.get("metadata", None)

    @client_initialized_decorator
    def get_task_metadata(self, task_id, qpu_id: str = None):
        """
        The results from this endpoint are the compilation metadata passed through at
        the time of task submission, not additional metadata about the task
        itself. See the metrics for that.
        """
        server = self._get_qpu_endpoint(qpu_id)
        endpoint = f"{server}/tasks/{str(task_id)}/metadata"
        metadata = self._get(endpoint).json()
        return self._get_task_metadata(metadata)

    @client_initialized_decorator
    def get_task_timings(self, task_id, qpu_id: str = None):
        server = self._get_qpu_endpoint(qpu_id)
        endpoint = f"{server}/tasks/{str(task_id)}/timings"
        metadata = self._get(endpoint).json()
        return metadata.get("timings", None)

    @client_initialized_decorator
    def get_task_execution_estimates(
        self, task_ids: Union[uuid4, list[uuid4]], qpu_id: str
    ):
        if not isinstance(task_ids, list):
            task_ids = [task_ids]
        server = self._get_qpu_endpoint(qpu_id)
        endpoint = f"{server}/monitoring/task_wait_time"
        json_body = {"task_ids": [str(id) for id in task_ids], "qpu_id": qpu_id}
        return self._post(
            endpoint,
            json=json_body,
        ).json()

    @default_qpu_id_decorator
    @client_initialized_decorator
    def get_qpu_execution_estimates(self, qpu_ids: Union[str, list[str]] = None):
        if qpu_ids is None:
            qpu_ids = self.default_qpu_id
        if not isinstance(qpu_ids, list):
            qpu_ids = [qpu_ids]

        # split the list of qpus by server
        split_qpus = defaultdict(list)

        for qpu_id in qpu_ids:
            try:
                qpu_url = self._get_qpu_endpoint(qpu_id)
                split_qpus[qpu_url].append(qpu_id)
            except ValueError as e:
                warnings.warn(f"Unable to estimate task execution, with exception {e}")

        response = {"qpu_wait_times": []}
        for server, qpu_list in split_qpus.items():
            json_message = {"targets": [str(id) for id in qpu_list]}
            resp1 = self._post(
                server + "/monitoring/qpu_wait_time",
                json=json_message,
            ).json()
            if "qpu_wait_times" in resp1 and resp1["qpu_wait_times"] is not None:
                for wait_time in resp1["qpu_wait_times"]:
                    response["qpu_wait_times"].append(wait_time)

        return response

    @client_initialized_decorator
    def cancel_task(self, task_ids: Union[uuid4, list[uuid4]], qpu_id: str = None):
        if not isinstance(task_ids, list):
            task_ids = [task_ids]
        try:
            server = self._get_qpu_endpoint(qpu_id)
            endpoint = f"{server}/tasks/cancel_many"
        except ValueError as e:
            warnings.warn(f"Unable to cancel a task, with exception {e}")

        return self._post(endpoint, json={"tasks": [str(id) for id in task_ids]})

    @client_initialized_decorator
    def create_user(self, name, email, password=None, validate=True):
        name_parts = name.split(" ", 1)
        first_name = ""
        last_name = ""
        if len(name_parts) == 1:
            first_name = name_parts[0]
            last_name = name_parts[0]
        elif len(name_parts) > 1:
            first_name = name_parts[0]
            last_name = name_parts[1]
        else:
            raise ValueError("Name must be provided")
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": _validated_email(email) if validate else email,
            "password": "" if not password else password,
        }
        return self._post("/admin/users", json=payload).json()


def _validate_datetime_format(time: str) -> Optional[datetime]:
    try:
        datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        return time
    except ValueError as e:
        warnings.warn(f"Unable to convert {time} to a datetime, with exception {e}")
        return None


def _validated_email(email: str) -> str:
    pattern = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if not re.fullmatch(pattern, email):
        raise ValueError(f"{email} does not appear to be a valid email")
    return email


def _validated_url(url: str) -> str:
    if urlparse(url).scheme not in ["http", "https"]:
        raise ValueError(f"{url} does not appear to be a valid url")
    return url.rstrip("/")


def _validated_name(name: str) -> str:
    if len(name.strip()) < 1:
        raise ValueError(f"Invalid user name: {name}")
    return name


def _validated_password(password: str) -> str:
    if len(password.strip()) == 0:
        raise ValueError("provided an empty password field.")
    return password
