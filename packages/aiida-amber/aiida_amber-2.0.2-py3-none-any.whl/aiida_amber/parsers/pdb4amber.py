"""
Parsers provided by aiida_amber.

This calculation configures the ability to use the 'pdb4amber' executable.
"""
import os
from pathlib import Path

from aiida.common import exceptions
from aiida.engine import ExitCode
from aiida.orm import SinglefileData
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory

from aiida_amber.utils import node_utils

Pdb4amberCalculation = CalculationFactory("amber.pdb4amber")


class Pdb4amberParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a Pdb4amberCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, Pdb4amberCalculation):
            raise exceptions.ParsingError("Can only parse Pdb4amberCalculation")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        # the directory for storing parsed output files
        output_dir = Path(self.node.get_option("output_dir"))

        # Grab list of retrieved files.
        files_retrieved = self.retrieved.base.repository.list_object_names()

        # Grab list of files expected and remove the scheduler stdout and stderr files.
        files_expected = [
            files
            for files in self.node.get_option("retrieve_list")
            if files not in ["_scheduler-stdout.txt", "_scheduler-stderr.txt"]
        ]

        # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = ["pdb4amber.out"]
        if "pdb4amber_outfiles" in self.node.inputs:
            for name in self.node.inputs.pdb4amber_outfiles:
                files_expected.extend([str(name)])


        # Check if the expected files are a subset of retrieved.
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(
                f"Found files '{files_retrieved}', expected to find '{files_expected}'"
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # passing along all expected output file as SinglefileData nodes.
        for thing in files_expected:
            self.logger.info(f"Parsing '{thing}'")
            with self.retrieved.open(thing, "rb") as handle:
                output_node = SinglefileData(file=handle, filename=thing)
            if thing == "pdb4amber.out":
                self.out("stdout", output_node)
            else:
                self.out(node_utils.format_link_label(thing), output_node)

        # If not in testing mode, then copy back the files.
        if "PYTEST_CURRENT_TEST" not in os.environ:
            self.retrieved.copy_tree(output_dir)

        return ExitCode(0)
