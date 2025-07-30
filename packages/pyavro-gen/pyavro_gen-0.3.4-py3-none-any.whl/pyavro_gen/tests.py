#!/usr/bin/env python3
"""
Test class for the Avro classes generator.
"""

__author__ = "Nicola Bova"
__copyright__ = "Copyright 2019, Jaumo GmbH"
__email__ = "nicola.bova@jaumo.com"

import unittest
from pathlib import Path

from avro_preprocessor.avro_paths import AvroPaths

from pyavro_gen.generator import AvroGenerator

ROOT_DIR = Path(__file__).absolute().parent.parent


class AvroPreprocessorTest(unittest.TestCase):
    """
    Test class for the Avro schema extension.
    """

    @staticmethod
    def test_fixtures() -> None:
        """
        Standard test.
        """
        generator = AvroGenerator(
            AvroPaths(
                input_path=str(ROOT_DIR.joinpath('fixtures/')),
                output_path=str(ROOT_DIR.joinpath('avroclasses/')),
                input_schema_file_extension='avsc',
                base_namespace='com.jaumo.schema',
                rpc_namespace='com.jaumo.schema.rpc',
                types_namespace='com.jaumo.schema.type',
            )
        )

        generator.process()
