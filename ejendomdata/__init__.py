from __future__ import annotations
from .propertydata import *
from .api import search_for_address
from .setup_logging import _setup_logging
_setup_logging(debug=False)

__all__ = [*propertydata.__all__, "get_address"]

def get_address(address: str) -> PropertyAddress:
    address = search_for_address(address)
    return PropertyAddress(address[0]["id"])