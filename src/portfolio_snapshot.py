from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Iterable


@dataclass(frozen=True)
class Holding:
    owner: str
    instrument: str
    platform: str
    value_idr: Decimal
    as_of: date

    def __post_init__(self) -> None:
        if not self.owner.strip() or not self.instrument.strip() or not self.platform.strip():
            raise ValueError("owner, instrument, and platform are required")
        if self.value_idr.is_nan() or self.value_idr.is_infinite() or self.value_idr < 0:
            raise ValueError("value_idr must be finite and non-negative")


def _money(value: Decimal | int | str) -> Decimal:
    try:
        parsed = value if isinstance(value, Decimal) else Decimal(str(value).replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"invalid money value: {value!r}") from exc
    if parsed.is_nan() or parsed.is_infinite():
        raise ValueError("money value must be finite")
    return parsed


def load_rows(rows: Iterable[dict[str, object]], as_of: date) -> list[Holding]:
    if not isinstance(as_of, date):
        raise TypeError("as_of must be a date")
    holdings = [
        Holding(
            owner=str(row.get("owner", "")),
            instrument=str(row.get("instrument", "")),
            platform=str(row.get("platform", "")),
            value_idr=_money(row.get("value_idr", "")),
            as_of=as_of,
        )
        for row in rows
    ]
    if not holdings:
        raise ValueError("at least one holding is required")
    return holdings


def totals_by(holdings: Iterable[Holding], field: str) -> dict[str, Decimal]:
    if field not in {"owner", "instrument", "platform"}:
        raise ValueError("field must be owner, instrument, or platform")
    totals: dict[str, Decimal] = {}
    for holding in holdings:
        key = getattr(holding, field)
        totals[key] = totals.get(key, Decimal("0")) + holding.value_idr
    return dict(sorted(totals.items()))


def total_value(holdings: Iterable[Holding]) -> Decimal:
    return sum((holding.value_idr for holding in holdings), Decimal("0"))


def allocation(holdings: Iterable[Holding]) -> dict[str, Decimal]:
    items = list(holdings)
    total = total_value(items)
    if total <= 0:
        raise ValueError("total value must be positive")
    return {key: value / total for key, value in totals_by(items, "instrument").items()}


def markdown_report(holdings: Iterable[Holding]) -> str:
    items = list(holdings)
    total = total_value(items)
    owners = totals_by(items, "owner")
    lines = [
        f"# Portfolio snapshot — {items[0].as_of.isoformat()}",
        "",
        f"Total recorded value (IDR): Rp{total:,.0f}",
        "",
        "| Owner | Instrument | Platform | Value (IDR) |",
        "| --- | --- | --- | ---: |",
    ]
    lines.extend(
        f"| {h.owner} | {h.instrument} | {h.platform} | Rp{h.value_idr:,.0f} |"
        for h in items
    )
    lines.extend(["", "## Totals by owner", "", "| Owner | Value (IDR) |", "| --- | ---: |"])
    lines.extend(f"| {owner} | Rp{value:,.0f} |" for owner, value in owners.items())
    return "\n".join(lines) + "\n"


# ponytail: keep this module stdlib-only until a real import source needs schema mapping.
