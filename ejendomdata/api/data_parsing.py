from __future__ import annotations
from . import api
import re

__all__ = [
    "parse_sales_history",
    "parse_general_info",
    "parse_valuation_history"
    ]


def _format_amount(amount: str) -> float:
    amount = re.sub(r'[^\d,.-]', '', amount)
    
    if "," in amount and "." in amount:
        amount = amount.replace(".", "").replace(",", ".")
    elif "," in amount:
        amount = amount.replace(",", ".")

    try:
        return float(amount)
    except ValueError:
        return 0.0


def parse_sales_history(address_history: dict) -> list[dict[str, int | str]]:
    salg_list = address_history.get("salgList")
    if not salg_list:
        return []

    results = []
    for sale in salg_list:
        sales_record = api.get_sales_info(sale["salgs_id"])
        hissalg: dict = sales_record.get("hissalgMain", {})
        hissalg["salg_id"] = sales_record.get("salg_id")

        for key in ("koebesum_beloeb", "kontant_koebesum", "kontant_pris"):
            hissalg[key] = _format_amount(hissalg.get(key, "0"))

        hissalg["overdragelses_tekst"] = hissalg.get("overdragelses_tekst", "").strip()
        results.append(hissalg)

    return results 


def parse_valuation_history(address_history: dict):
    valuation_list = address_history.get("vurdList")
    
    if not valuation_list:
        return []
    
    results = []

    for valuation in valuation_list:
        valuation_record = api.get_valuation_info(valuation["vur_id"])
        hisvurd: dict = valuation_record.get("hisvurdDataMain", {})
        hisvurd["vurd_id"] = valuation_record.get("vurd_id")

        for key, value in hisvurd.items():
            if isinstance(value, str):
                hisvurd[key] = value.strip()
        results.append(hisvurd)
    return results


def parse_general_info(general_info: dict[str, None | int | dict], bfe: int | str) -> dict[str, int | str | list]:
    if general_info["GeneralInfoSFE"] is not None:
        if general_info["GeneralInfoSFE"]["bfeNummer"] == int(bfe):
            return general_info["GeneralInfoSFE"]
    
    if general_info["GeneralInfoBPFG"] is not None:
        if general_info["GeneralInfoBPFG"]["bfeNummer"] == int(bfe):
            return general_info["GeneralInfoBPFG"]
    
    if general_info["GeneralInfoEJL"] is not None:
        if general_info["GeneralInfoEJL"]["bfeNummer"] == int(bfe):
            return general_info["GeneralInfoEJL"]
    return dict()
    
    
    
    
    

