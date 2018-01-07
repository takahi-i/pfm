#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pfm` package."""


import unittest
from click.testing import CliRunner

from pf_manager import cli


class TestPfm(unittest.TestCase):
    """Tests for `pfm` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'port forwarding manager' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help' in help_result.output
