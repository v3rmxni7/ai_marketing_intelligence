# src/utils.py

import json
from pprint import pprint
from typing import Any


def load_json(path: str) -> Any:
    """
    Load a JSON file safely.
    Used for loading transactions, customers, campaigns.
    """
    with open(path, "r") as f:
        return json.load(f)


def pretty_print(title: str, data: Any) -> None:
    """
    Pretty-print sections in console output.
    Useful for pipeline debugging & demos.
    """
    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)
    pprint(data)
    print("=" * 60 + "\n")


def safe_divide(numerator: float, denominator: float) -> float:
    """
    Prevent ZeroDivisionError in ROI / rate calculations.
    """
    if denominator == 0:
        return 0.0
    return numerator / denominator


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a numeric value between min and max.
    Useful for rates like participation, ROI caps, etc.
    """
    return max(min_value, min(value, max_value))
