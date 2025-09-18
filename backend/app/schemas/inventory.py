from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import date

class InventoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None

class InventoryCreate(InventoryBase):
    manager_id: Optional[int] = None

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    manager_id: Optional[int] = None
    status: Optional[str] = None

class InventoryResponse(InventoryBase):
    id: int
    school_id: int
    manager_id: Optional[int]
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True

class InventoryItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    sku: Optional[str] = None
    unit: Optional[str] = None
    current_stock: float = 0
    minimum_stock: float = 0
    maximum_stock: Optional[float] = None
    unit_cost: Optional[float] = None
    supplier: Optional[str] = None

class InventoryItemCreate(InventoryItemBase):
    inventory_id: int

class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    sku: Optional[str] = None
    unit: Optional[str] = None
    current_stock: Optional[float] = None
    minimum_stock: Optional[float] = None
    maximum_stock: Optional[float] = None
    unit_cost: Optional[float] = None
    supplier: Optional[str] = None
    status: Optional[str] = None

class InventoryItemResponse(InventoryItemBase):
    id: int
    school_id: int
    inventory_id: int
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True