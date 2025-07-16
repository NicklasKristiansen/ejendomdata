from __future__ import annotations
from . import api
import re

__all__ = ["parse_sales_history"]


def _format_amount(amount: str) -> float:
    cleaned = re.sub(r'[^\d,.-]', '', amount)
    return float("".join(e if e.isdigit() else "." if e == "," else ""  for e in cleaned))



def parse_sales_history(property_history: dict) -> list[dict[str, int | str]] | list[None]:
    sales_history: list[dict[str, int | str]] = property_history.get("salgList", None)
    if not sales_history:
        return list()
    
    sales_history = [api.get_sales_info(sale["salgs_id"]) for sale in sales_history]
    
    for i, sales_record in enumerate(sales_history):
        sales_record["hissalgMain"]["salg_id"] = sales_record["salg_id"]
        sales_record = sales_record["hissalgMain"]
        
        for element in ("koebesum_beloeb", "kontant_koebesum", "kontant_pris"):
            sales_record[element] = _format_amount(sales_record[element])
        sales_record["overdragelses_tekst"] = sales_record["overdragelses_tekst"].strip()
        
        sales_history[i] = sales_record
    return sales_history    

