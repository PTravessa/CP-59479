import unittest
from datetime import datetime
from trotinette import Trotinette
import time

t1 = Trotinette(1000, 0.25)
t2 = Trotinette(1001, 0.25)


class TestTrotinetteMethods(unittest.TestCase):

    def test__str__(self):
        t1 = Trotinette(1234, 0.25)
        expected = "1234_Benefit_0"
        self.assertEqual(str(t1), expected)

    def test_check_in1(self):
        date = datetime.now()
        t1.check_in(100)
        delta = t1.rent_timestamp_start - date
        self.assertTrue(delta.seconds >= 0 and delta.seconds < 5)

    def test_check_in2(self):
        with self.assertRaises(AssertionError):
            t1.check_in(100)

    def test_check_in3(self):
        t2.check_in(101)
        self.assertEqual(t1.user_id, 100)
        
    @unittest.skip
    def test_check_out1(self):
        time.sleep(5)
        date = datetime.now()
        t1.check_out()
        duration = (date - t1.rent_timestamp_start).seconds
        self.assertTrue(abs(duration - 5) < 0.1)

    @unittest.skip
    def test_check_out2(self):
        self.assertFalse(t1.in_use())

    @unittest.skip
    def test_check_out3(self):
        time.sleep(2*60)
        total = t2.total_benefit
        t2.check_out()
        total_after = t2.total_benefit
        duration = t2.rent_timestamp_end - t2.rent_timestamp_start
        duration = round(duration.seconds/60)
        value = t2.cost_per_minute * duration
        self.assertTrue(total_after - total == value)


if __name__ == '__main__':
    unittest.main()
