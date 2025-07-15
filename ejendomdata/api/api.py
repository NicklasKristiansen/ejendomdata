from urllib.parse import quote_plus
from ..constants import *
import httpx

__all__ = [
    "get_bfe",
    "search_for_address",
    "get_address_history"
]

def search_for_address(addresse: str):
    response = httpx.get(url=_DATAFORSYNING_URL_ + f"adresser?q={quote_plus(addresse)}").raise_for_status()
    return response.json()


def get_bfe(adress_id: str):
    response = httpx.get(url=_OIS_BASE_URL_ + "property/" + f"GetBFEFromAddressId?addressId={adress_id}")
    return response.json()


def get_address_history(bfe: str | int):
    response = httpx.get(url=_OIS_BASE_URL_ + "svur/" + f"get?bfe={bfe}").raise_for_status()
    return response.json()





