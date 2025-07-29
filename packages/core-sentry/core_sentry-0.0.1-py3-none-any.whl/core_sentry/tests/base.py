# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch, Mock


class BaseSentryTestCases(TestCase):
    """ Base class for Test Cases related to Sentry integration """

    sentry_patcher = patch(target="sentry_sdk.init")
    sentry_mock = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.sentry_mock = cls.sentry_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.sentry_patcher.stop()
