"""
TestIndex CLI commands.

This module provides the command-line interface for TestIndex.
"""

from aston.cli.commands.init import init_command
from aston.cli.commands.coverage import coverage_command
from aston.cli.commands.test import test_command
from aston.cli.commands.graph import graph_command
from aston.cli.commands.check import check_command
from aston.cli.commands.ingest_coverage import ingest_coverage_command
from aston.cli.commands.test_suggest import test_suggest_command
from aston.cli.commands.regression_guard import regression_guard_command
from aston.cli.commands.criticality import criticality
from aston.cli.commands.cache import cache_group

# List of commands to register with CLI
commands = [
    init_command,
    test_command,
    coverage_command,
    graph_command,
    check_command,
    ingest_coverage_command,
    test_suggest_command,
    regression_guard_command,
    criticality,
    cache_group,
] 