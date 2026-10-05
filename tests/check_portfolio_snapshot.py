from datetime import date
from decimal import Decimal

from src.portfolio_snapshot import allocation, load_rows, markdown_report, total_value, totals_by


def check() -> None:
    as_of = date(2026, 9, 17)
    rows = [
        {"owner": "user", "instrument": "VTI", "platform": "broker", "value_idr": "100.00"},
        {"owner": "wife", "instrument": "VTI", "platform": "broker", "value_idr": "50.00"},
        {"owner": "user", "instrument": "unit link", "platform": "insurer", "value_idr": "25.00"},
    ]
    holdings = load_rows(rows, as_of)
    assert total_value(holdings) == Decimal("175.00")
    assert totals_by(holdings, "owner") == {"user": Decimal("125.00"), "wife": Decimal("50.00")}
    assert totals_by(holdings, "instrument")["VTI"] == Decimal("150.00")
    assert sum(allocation(holdings).values()) == Decimal("1")
    assert markdown_report(holdings) == markdown_report(load_rows(rows, as_of))
    for bad in ("NaN", "Infinity", "-1", "invalid"):
        try:
            load_rows([{"owner": "user", "instrument": "VTI", "platform": "broker", "value_idr": bad}], as_of)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted invalid value {bad!r}")
    try:
        load_rows([], as_of)
    except ValueError:
        pass
    else:
        raise AssertionError("accepted empty snapshot")


if __name__ == "__main__":
    check()
    print("portfolio snapshot checks passed")
