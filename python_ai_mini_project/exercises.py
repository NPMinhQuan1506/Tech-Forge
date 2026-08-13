class BankAccount:
    """Simple bank account for practicing class, method, and property."""

    def __init__(self, owner: str, balance: float = 0) -> None:
        if not owner or not owner.strip():
            raise ValueError("Owner must not be empty.")
        if balance < 0:
            raise ValueError("Initial balance must not be negative.")

        self.owner = owner.strip()
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self._balance:
            raise ValueError("Insufficient balance.")
        self._balance -= amount


def check_number(number: int) -> dict:
    """
    Return sign and parity of a number.

    Expected:
    check_number(4) -> {"sign": "positive", "parity": "even"}
    check_number(-3) -> {"sign": "negative", "parity": "odd"}
    check_number(0) -> {"sign": "zero", "parity": "even"}
    """
    if number > 0:
        sign = "positive"
    elif number < 0:
        sign = "negative"
    else:
        sign = "zero"

    parity = "even" if number % 2 == 0 else "odd"
    return {"sign": sign, "parity": parity}


def even_squares(numbers: list[int]) -> list[int]:
    """
    Return squares of even numbers only.

    Expected:
    even_squares([4, 7, 2, 9, 10, 3]) -> [16, 4, 100]
    """
    return [number**2 for number in numbers if number % 2 == 0]


def summarize_numbers(raw_numbers: str) -> dict:
    """
    Parse comma-separated numbers and return summary.

    Expected:
    summarize_numbers("1,2,3") -> {
        "total": 6.0,
        "average": 2.0,
        "max": 3.0,
        "min": 1.0,
    }

    Ignore empty items like "1, 2, , 3".
    Raise ValueError if there is no valid number.
    """
    numbers = [float(item.strip()) for item in raw_numbers.split(",") if item.strip()]
    if not numbers:
        raise ValueError("Provide at least one valid number.")

    total = sum(numbers)
    return {
        "total": total,
        "average": total / len(numbers),
        "max": max(numbers),
        "min": min(numbers),
    }
