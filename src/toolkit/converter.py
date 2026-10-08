from .constants import CFG
from .errors import ConvErr


def conv_temp(val: float, u_from: str, u_to: str) -> float:
    """конвертация температур c проверкой абсолютного нуля"""
    if (u_from == "c" and val < -273.15) or \
            (u_from == "k" and val < 0) or \
            (u_from == "f" and val < -459.67):
        raise ConvErr("температура ниже абсолютного нуля")

    if u_from == "c":
        c_val = val
    elif u_from == "k":
        c_val = val - 273.15
    elif u_from == "f":
        c_val = (val - 32) * 5 / 9
    else:
        raise ConvErr(f"неизвестная единица: {u_from}")

    if u_to == "c":
        return float(c_val)
    elif u_to == "k":
        return float(c_val + 273.15)
    elif u_to == "f":
        return float(c_val * 9 / 5 + 32)
    else:
        raise ConvErr(f"неизвестная единица: {u_to}")

def convert(val: float, u_from: str, u_to: str) -> float:
    """функция конвертера"""
    u_from = u_from.lower()
    u_to = u_to.lower()
    temps = {"c", "f", "k"}
    if u_from in temps and u_to in temps:
        return conv_temp(val, u_from, u_to)
    cat = None
    for k in CFG:
        if u_from in CFG[k] and u_to in CFG[k]:
            cat = k
            break
    if not cat:
        raise ConvErr("несовместимые или неизвестные единицы")
    res = val * CFG[cat][u_from] / CFG[cat][u_to]
    return float(res)