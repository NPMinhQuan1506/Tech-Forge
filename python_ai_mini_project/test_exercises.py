import unittest

from exercises import BankAccount, check_number, even_squares, summarize_numbers


class TestExercises(unittest.TestCase):
    def test_check_number(self):
        self.assertEqual(check_number(4), {"sign": "positive", "parity": "even"})
        self.assertEqual(check_number(-3), {"sign": "negative", "parity": "odd"})
        self.assertEqual(check_number(0), {"sign": "zero", "parity": "even"})

    def test_even_squares(self):
        self.assertEqual(even_squares([4, 7, 2, 9, 10, 3]), [16, 4, 100])
        self.assertEqual(even_squares([1, 3, 5]), [])
        self.assertEqual(even_squares([]), [])

    def test_summarize_numbers(self):
        self.assertEqual(
            summarize_numbers("1,2,3"),
            {"total": 6.0, "average": 2.0, "max": 3.0, "min": 1.0},
        )
        self.assertEqual(
            summarize_numbers("10, 20, , 30"),
            {"total": 60.0, "average": 20.0, "max": 30.0, "min": 10.0},
        )
        with self.assertRaises(ValueError):
            summarize_numbers(" , , ")

    def test_bank_account(self):
        account = BankAccount("Quan", 100)
        self.assertEqual(account.owner, "Quan")
        self.assertEqual(account.balance, 100)

        account.deposit(50)
        self.assertEqual(account.balance, 150)

        account.withdraw(40)
        self.assertEqual(account.balance, 110)

        with self.assertRaises(ValueError):
            account.withdraw(999)

        with self.assertRaises(ValueError):
            account.deposit(-1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
