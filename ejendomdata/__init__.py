from __future__ import annotations
from .constants import *
from .api import *
from .propertydata import *
from .setup_logging import _setup_logging
_setup_logging(debug=False)

def get_address(address: str) -> PropertyAddress:
    address = search_for_address(address)
    return PropertyAddress(address[0]["id"])