from __future__ import annotations
from urllib.parse import quote_plus
from functools import wraps
import time
import logging
from ..constants import *
from .status_code_handler import *
import httpx

logger = logging.getLogger(__name__)
__all__ = [
    "get_bfe",
    "search_for_address",
    "get_address_history",
    "get_general_info",
    "get_sales_info",
    "get_valuation_info"
]



def search_for_address(addresse: str) -> dict:
    response = httpx.get(url=_DATAFORSYNING_URL_ + f"adresser?q={quote_plus(addresse)}")
    return status_code_handler(response).json()


def get_bfe(address_id: str) -> int:
    response = httpx.get(url=_OIS_BASE_URL_ + "property/" + f"GetBFEFromAddressId?addressId={address_id}")
    return status_code_handler(response).json()


def get_address_history(bfe: str | int) -> dict:
    response = httpx.get(url=_OIS_BASE_URL_ + "svur/" + f"get?bfe={bfe}")
    return status_code_handler(response).json()

def get_general_info(bfe: str | int) -> dict:
    response = httpx.get(url=_OIS_BASE_URL_ + "property/" + f"GetGeneralInfoFromBFE?bfe={bfe}")
    return status_code_handler(response).json()


def get_sales_info(sales_id: int | str) -> dict:
    response = httpx.get(url=_OIS_BASE_URL_ + "svur/" + f"GetSalg?salgId={sales_id}")
    return status_code_handler(response).json()
    

def get_valuation_info(valuation_id: int | str) -> dict:
    response = httpx.get(url=_OIS_BASE_URL_ + "svur/" + f"GetVurdering?vurdId={valuation_id}")
    return status_code_handler(response).json()


    

