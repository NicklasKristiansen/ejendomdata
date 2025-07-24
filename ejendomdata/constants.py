from __future__ import annotations
__all__ = [
    "_OIS_BASE_URL_",
    "_DAR_BFE_PUBLIC_URL_",
    "_DATAFORSYNING_URL_",
    "VALID_STATUS_RESPONSES"
]
_OIS_BASE_URL_ = "https://ois.dk/api/"
_DATAFORSYNING_URL_ = "https://api.dataforsyningen.dk/"
_DAR_BFE_PUBLIC_URL_ = "https://services.datafordeler.dk/DAR/DAR_BFE_Public/1/rest/"


VALID_STATUS_RESPONSES = (200, 202, 204)