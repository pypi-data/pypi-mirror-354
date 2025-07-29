# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Oxford Quantum Circuits Ltd
import argparse
import json
import os.path
import sys
from getpass import getpass

from qcaas_client.client import (
    ExperimentalConfig,
    OQCClient,
    QPUTask,
    QuantumResultsFormat,
)


class OQCCommands:
    parser = argparse.ArgumentParser(
        description="OQC Cloud Client CLI.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-u", "--url", default="http://localhost:4000")
    parser.add_argument("-t", "--auth_token", help="Authentication token.")
    parser.add_argument("-q", "--qpu_id", type=str, default=None)

    subparsers = parser.add_subparsers(dest="command", help="Command to execute.")
    _run_qasm = subparsers.add_parser(
        "run_qasm",
        help="Submit and run QASM file on OQC Cloud.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    _run_qasm.add_argument("-p", "--path", default=os.getcwd())
    _run_qasm.add_argument("-f", "--file", action="append", default=[])
    _run_qasm.add_argument("-s", "--shots", type=int, default=1000)
    _run_qasm.add_argument(
        "-o",
        "--output",
        default="BinaryCount",
        choices=["Raw", "Binary", "BinaryCount"],
    )
    _run_qasm.add_argument(
        "--noise",
        action="store_true",
        help="Apply the Toshiko noise model (Fermioniq-only).",
    )
    _run_qasm.add_argument(
        "--bond_dimension",
        type=int,
        default=None,
        help="Bond dimension to use for DMRG mode (Fermioniq-only).",
    )
    _run_qasm.add_argument(
        "--noise_model", type=str, default=None, help="Path to a noise model JSON file."
    )
    basic_qasm = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
rx(0.01) q[0];
measure q[0]->c[0];
"""

    def __init__(self, args):
        self.args = self.validate_run(args)
        self.qc = OQCClient(
            url=self.args.url, authentication_token=self.args.auth_token
        )

    @staticmethod
    def read_program(program_filename):
        if not os.path.exists(program_filename):
            raise ValueError(f"{program_filename} doesn't exist as a path.")

        with open(program_filename, "r") as f:
            program = f.read()
        return program

    def run_qasm(self, args):
        tasks = []  # an array of {program, metadata} objects that define a TASK
        results_format = QuantumResultsFormat()
        if args.output == "Binary":
            results_format.binary()
        elif args.output == "Raw":
            results_format.raw()
        else:
            results_format.binary_count()
        # load noise model JSON file
        nm_json = None
        if args.noise_model:
            nm_text = OQCCommands.read_program(
                os.path.join(args.path, args.noise_model)
            )
            try:
                nm_json = json.loads(nm_text)
            except json.JSONDecodeError:
                raise ValueError("Noise model file is not valid JSON.")
        if nm_json and not args.noise:
            args.noise = True
        config = ExperimentalConfig(
            repeats=args.shots,
            results_format=results_format,
            noise=args.noise,
            bond_dimension=args.bond_dimension,
            noise_model=nm_json,
        )
        for filename in args.file:
            program = OQCCommands.read_program(os.path.join(args.path, filename))
            tasks.append(QPUTask(program=program, config=config))

        # If we have no tasks just default with a very basic QASM program.
        if not any(tasks):
            tasks.append(QPUTask(OQCCommands.basic_qasm, config))

        sys.stdout.write("Executing tasks...\n")
        results = self.qc.execute_tasks(tasks, qpu_id=args.qpu_id)
        for res in results:
            if res.has_errored():
                sys.stdout.write(str(res.error_details.error_message) + "\n")
            else:
                sys.stdout.write(str(res.result) + "\n")

    @staticmethod
    def validate_run(args):
        if args.command is None:
            args.command = "run_qasm"
            args.path = getattr(args, "path", os.path.dirname(__file__))
            args.file = getattr(args, "file", [])
            args.shots = getattr(args, "shots", 1000)
            args.output = getattr(args, "output", "BinaryCount")
            args.qpu_id = getattr(args, "qpu_id", None)
            args.noise = getattr(args, "noise", False)
            args.bond_dimension = getattr(args, "bond_dimension", None)
            args.noise_model = getattr(args, "noise_model", None)
        if args.auth_token is None:
            args.auth_token = getpass("Auth Token: ")

        return args


def run(args):
    oqc_commands = OQCCommands(args)

    sys.stdout.write(f"Attempting to connect to {args.url}\n")
    if args.command == "run_qasm":
        oqc_commands.run_qasm(args=args)
    else:
        args.print_help()


def main():
    args = OQCCommands.parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
