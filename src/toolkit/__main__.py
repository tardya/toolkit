import argparse
import sys

from .calculator import calculate
from .converter import convert
from .errors import ToolkitErr


def main() -> None:
    """вход в приложение"""
    p = argparse.ArgumentParser(prog="toolkit", description="набор консольных утилит")
    sub_p = p.add_subparsers(dest="cmd", required=True)

    c_p = sub_p.add_parser("calc", help="калькулятор выражений")
    c_p.add_argument("expr", type=str, help="строка с математическим выражением")

    cv_p = sub_p.add_parser("convert", help="конвертер величин")
    cv_p.add_argument("val", type=float, help="числовое значение")
    cv_p.add_argument("u_from", type=str, help="исходная единица измерения")
    cv_p.add_argument("u_to", type=str, help="искомая единица измерения")

    try:
        args = p.parse_args()
        if args.cmd == "calc":
            res = calculate(args.expr)
            print(res)
        elif args.cmd == "convert":
            res = convert(args.val, args.u_from, args.u_to)
            print(res)
        sys.exit(0)
    except ToolkitErr as e:
        print(f"ошибка: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"неизвестная ошибка: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()