import decimal
import json
import math

from decimal import Decimal
from pathlib import Path

from .errors import CalcErr

decimal.getcontext().rounding = decimal.ROUND_HALF_UP
HIST_FILE = Path("history.json")

def save_hist(expr: str, res: str) -> None:
    """сохраняет историю успешных вычислений в json"""
    hist = []
    if HIST_FILE.exists():
        try:
            with open(HIST_FILE, "r", encoding="utf-8") as f:
                hist = json.load(f)
        except json.JSONDecodeError:
            pass
    hist.append({"expr": expr, "res": res})
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=4)

def tokenize(expr: str) -> list[str]:
    """токенизация: разбивает строку на числа, операторы и скобки"""
    if not expr.strip():
        raise CalcErr("пустое выражение")

    toks = []
    i = 0
    n = len(expr)

    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c in "+-*/%()":
            if c == "/" and i + 1 < n and expr[i + 1] == "/":
                toks.append("//")
                i += 2
                continue
            toks.append(c)
            i += 1
            continue
        if c.isdigit() or c == '.':
            start = i
            dots = 0
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    dots += 1
                i += 1
            if dots > 1:
                raise CalcErr("неверное числовое значение")
            toks.append(expr[start:i])
            continue
        raise CalcErr(f"недопустимый символ: {c}")
    return toks


def validate(toks: list[str]) -> list[str]:
    """проверяет токены и обрабатывает унарные плюсы и минусы"""
    if not toks:
        raise CalcErr("пустое выражение")

    ops = {"+", "-", "*", "/", "//", "%"}
    res = []

    for i, t in enumerate(toks):
        if t in ops:
            is_un = (i == 0) or (toks[i - 1] in ops) or (toks[i - 1] == "(")
            if is_un:
                if t == "+":
                    res.append("u+")
                elif t == "-":
                    res.append("u-")
                else:
                    raise CalcErr("пропущенный операнд")
            else:
                res.append(t)
        else:
            res.append(t)
    if res[-1] in ops:
        raise CalcErr("пропущенный операнд")
    for i, t in enumerate(res):
        if t in ops and i > 0 and res[i - 1] in ops:
                raise CalcErr("два бинарных оператора подряд")
    return res

def to_rpn(toks: list[str]) -> list[str]:
    """переводит токены в обратную польскую запись"""
    pri = {"u+": 3, "u-": 3, "*": 2, "/": 2, "//": 2, "%": 2, "+": 1, "-": 1}
    out = []
    stack = []

    for t in toks:
        if t == "(":
            stack.append(t)
        elif t == ")":
            while stack and stack[-1] != "(":
                out.append(stack.pop())
            if not stack:
                raise CalcErr("несогласованные скобки")
            stack.pop()
        elif t not in pri:
            out.append(t)
        else:
            while stack and stack[-1] != "(" and pri.get(stack[-1], 0) >= pri[t]:
                out.append(stack.pop())
            stack.append(t)
    while stack:
        if stack[-1] == "(":
            raise CalcErr("несогласованные скобки")
        out.append(stack.pop())
    return out

def calc_rpn(rpn: list[str]) -> Decimal:
    """вычисляет значение по обратной польской записи"""
    stack = []
    for t in rpn:
        if t == "u+":
            pass
        elif t == "u-":
            if not stack:
                raise CalcErr("пропущенный операнд")
            stack.append(-stack.pop())
        elif t in {"+", "-", "*", "/", "//", "%"}:
            if len(stack) < 2:
                raise CalcErr("пропущенный операнд")
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            elif t == "/":
                if b == 0: raise CalcErr("деление на ноль")
                stack.append(a / b)
            elif t == "//":
                if b == 0: raise CalcErr("деление на ноль")
                stack.append(Decimal(math.floor(a / b)))
            elif t == "%":
                if b == 0: raise CalcErr("деление на ноль")
                stack.append(a - (b * Decimal(math.floor(a / b))))
        else:
            try:
                stack.append(Decimal(t))
            except decimal.InvalidOperation:
                raise CalcErr("неверное числовое значение")
    if len(stack) != 1:
        raise CalcErr("пропущенный операнд")
    return stack[0]

def calculate(expr: str) -> str:
    """главная функция калькулятора"""
    toks = tokenize(expr)
    toks = validate(toks)
    rpn = to_rpn(toks)
    res = calc_rpn(rpn)
    str_res = str(res)
    save_hist(expr, str_res)
    return str_res