import unittest
from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        # Default to discovering tests from polls/tests/
        if not test_labels:
            test_labels = ['polls.tests']
        return super().build_suite(test_labels, extra_tests, **kwargs)
