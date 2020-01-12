import unittest
from core.dal.users import User


class ExampleTest(unittest.TestCase):

    def test_money_fail(self):
        user = User()

        with self.assertRaises(Exception) as context:
            do.something()
        self.assertEqual(context.exception.reason, 'not_enough_gold')
        self.assertIsNotNone(user)


if __name__ == '__main__':
    unittest.main()
