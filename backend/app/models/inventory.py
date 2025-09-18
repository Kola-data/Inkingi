from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Inventory(BaseModel):
    __tablename__ = "inventories"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(200), nullable=False)  # e.g., "Main Store", "Library Books"
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    manager_id = Column(Integer, ForeignKey("staff.id"), nullable=True)
    status = Column(String(20), default="active")  # active, inactive
    
    # Relationships
    school = relationship("School")
    manager = relationship("Staff")
    items = relationship("InventoryItem", back_populates="inventory")

class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventories.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # e.g., "Books", "Equipment", "Supplies"
    sku = Column(String(100), nullable=True)  # Stock Keeping Unit
    unit = Column(String(50), nullable=True)  # e.g., "pieces", "kg", "liters"
    current_stock = Column(Float, default=0)
    minimum_stock = Column(Float, default=0)
    maximum_stock = Column(Float, nullable=True)
    unit_cost = Column(Float, nullable=True)
    supplier = Column(String(200), nullable=True)
    status = Column(String(20), default="active")  # active, inactive, discontinued
    
    # Relationships
    school = relationship("School")
    inventory = relationship("Inventory", back_populates="items")
    stock_movements = relationship("StockMovement", back_populates="item")

class StockMovement(BaseModel):
    __tablename__ = "stock_movements"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    movement_type = Column(String(20), nullable=False)  # in, out, transfer, adjustment
    quantity = Column(Float, nullable=False)
    unit_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    reference = Column(String(100), nullable=True)  # Invoice number, etc.
    notes = Column(Text, nullable=True)
    movement_date = Column(Date, nullable=False)
    processed_by = Column(Integer, ForeignKey("staff.id"), nullable=True)
    
    # Relationships
    school = relationship("School")
    item = relationship("InventoryItem", back_populates="stock_movements")
    processor = relationship("Staff")