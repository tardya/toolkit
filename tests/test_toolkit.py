import subprocess

import pytest

from src.toolkit.calculator import calculate
from src.toolkit.errors import CalcErr


def test_sum():
    assert calculate("  2    +   2 ") == "4"

def test_priority():
    assert calculate("2 + 2 * 2") == "6"

def test_negative_res():
    assert calculate("10 - 25") == "-15"

def test_decimal():
    assert calculate("0.1 + 0.2") == "0.3"

def test_big_numbers():
    assert calculate("1000000000000 * 1000000000000") == "1000000000000000000000000"

def test_small_numbers():
    assert calculate("0.0000000001 + 0.0000000002") == "3E-10"

def test_integer_division():
    assert calculate("14 // 4") == "3"

def test_ost():
    assert calculate("14 % 4") == "2"

def test_combo():
    assert calculate("25 % 7 + 10 // 3") == "7"

def test_un_minus():
    assert calculate("-5 + 10") == "5"

def test_un_minus_inb():
    assert calculate("10 * (-2)") == "-20"

def test_brackets():
    assert calculate("((2 + 3) * (10 - 2)) // 4") == "10"

def test_unary():
    assert calculate("10 * -5") == "-50"

def test_err_div_zero():
    with pytest.raises(CalcErr, match="деление на ноль"):
        calculate("5 / 0")


def test_err_integer_div_zero():
    with pytest.raises(CalcErr, match="деление на ноль"):
        calculate("10 // 0")

def test_err_ost_zero():
    with pytest.raises(CalcErr, match="деление на ноль"):
        calculate("10 % 0")

def test_err_unmatched_brackets():
    with pytest.raises(CalcErr, match="несогласованные скобки"):
        calculate("2 + (3 * 4")

def test_err_skipped():
    with pytest.raises(CalcErr, match="пропущенный операнд"):
        calculate("2 + * 3")

def test_cli_calc_success():
    res = subprocess.run(
        ["python", "-m", "src.toolkit", "calc", "2+2"],
        capture_output=True, text=True, check=False
    )
    assert res.returncode == 0
    assert "4" in res.stdout

def test_cli_calc_fail():
    res = subprocess.run(
        ["python", "-m", "src.toolkit", "calc", "5/0"],
        capture_output=True, text=True, check=False
    )
    assert res.returncode == 2
    assert "деление на ноль" in res.stderr