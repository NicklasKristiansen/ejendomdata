from __future__ import annotations
from ..api import api, data_parsing
import uuid


class PropertyAddress:    
    def __init__(self, address_id: str):
        self._address_id = address_id
        self._validate_address_uuid()
        self._bfe = None
        self._address = None
        self._general_info = None
        self._entire_property_info = None
        self._sales_history = None
        self._address_history = None
        self._valuation_history = None
        
    def _validate_address_uuid(self):
        try:
            parsed = uuid.UUID(self._address_id)
            if str(parsed) != self._address_id.lower():
                raise ValueError("address_id has an incorrect format or case")
        except ValueError:
            raise ValueError(f"invalid address id: '{self._address_id}'")
    
    def _populate_general_info(self):
        self._entire_property_info = api.get_general_info(self.bfe)
        self._general_info = api.parse_general_info(self._entire_property_info, self.bfe)
        self._address = self._general_info["beligenhed"]
    
    
    def __eq__(self, other: PropertyAddress):
        return self.address_id == other.address_id
    
    
    def __repr__(self):
        return self.address
    
    
    @property
    def address_id(self):
        return self._address_id
    
    
    @property
    def bfe(self):
        if self._bfe is None:
            self._bfe = api.get_bfe(self.address_id)
        return self._bfe
    
    
    @property
    def address(self):
        if self._address is None:
            self._populate_general_info()
        return self._address
    
    
    @property
    def general_info(self):
        if self._general_info is None:
            self._populate_general_info()
        return self._general_info
           
    
    @property
    def entire_property_info(self):
        if self._entire_property_info is None:
            self._populate_general_info()
        return self._entire_property_info
           
           
    @property
    def address_history(self):
        if self._address_history is None:
            self._address_history = api.get_address_history(self.bfe)
        return self._address_history
            
    @property
    def sales_history(self):
        if self._sales_history is None:
            self._sales_history = data_parsing.parse_sales_history(self.address_history)
        return self._sales_history
    
    @property
    def valuation_history(self):
        if self._valuation_history is None:
            self._valuation_history = data_parsing.parse_valuation_history(self.address_history)
        return self._valuation_history
        
        
        


