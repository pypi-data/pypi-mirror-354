from unittest import TestCase
from datetime import datetime, timedelta, UTC

from shortcuts.date import time_now, time_in, time_ago, Config


class TestDate(TestCase):

    def test_methods(self):
        equal = self.compare

        # test time_now method
        equal(time_now(naive=True, utc=False), datetime.now())

        equal(time_now(naive=False, utc=False), datetime.now().astimezone())

        equal(time_now(naive=True, utc=True), datetime.now(UTC).replace(tzinfo=None))

        equal(time_now(naive=False, utc=True), datetime.now(UTC))

        # test time_in
        interval = {'seconds': 5, 'minutes': 1, 'hours': 2, 'days': 3, 'weeks': 4, 'microseconds': 5, 'milliseconds': 6}

        equal(time_in(naive=True, utc=False, **interval), datetime.now() + timedelta(**interval))

        equal(time_in(naive=False, utc=False, **interval), datetime.now().astimezone() + timedelta(**interval))

        equal(time_in(naive=True, utc=True, **interval), datetime.now(UTC).replace(tzinfo=None) + timedelta(**interval))

        equal(time_in(naive=False, utc=True, **interval), datetime.now(UTC) + timedelta(**interval))

        # test time_ago
        equal(time_ago(naive=True, utc=False, **interval), datetime.now() - timedelta(**interval))

        equal(time_ago(naive=False, utc=False, **interval), datetime.now().astimezone() - timedelta(**interval))

        equal(time_ago(naive=True, utc=True, **interval), datetime.now(UTC).replace(tzinfo=None) - timedelta(**interval))

        equal(time_ago(naive=False, utc=True, **interval), datetime.now(UTC) - timedelta(**interval))

        # test Config overrides
        Config.naive = True
        Config.utc = True
        equal(time_now(), datetime.now(UTC).replace(tzinfo=None))

        Config.naive = True
        Config.utc = False
        equal(time_in(**interval), datetime.now() + timedelta(**interval))

        Config.naive = False
        Config.utc = False
        equal(time_ago(**interval), datetime.now().astimezone() - timedelta(**interval))

        Config.naive = False
        Config.utc = True
        equal(time_now(), datetime.now(UTC))

    def compare(self, dt1, dt2):
        # ensure same data type
        self.assertIsInstance(dt1, type(dt2))

        # ensure tzinfo is the same
        self.assertEqual(dt1.tzinfo, dt2.tzinfo)

        # ensure datetime values are almost exactly same (account for execution time difference)
        self.assertLessEqual(abs(dt1 - dt2), timedelta(seconds=0.1))
