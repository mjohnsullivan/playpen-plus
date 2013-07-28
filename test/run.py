"""
Runs the test suite
"""
import unittest
from test_console_app import TestConsoleApp

tests = unittest.TestSuite((
    unittest.TestLoader().loadTestsFromTestCase(TestConsoleApp),
))

unittest.TextTestRunner(verbosity = 2).run(tests)