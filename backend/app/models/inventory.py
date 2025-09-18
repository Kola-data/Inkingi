from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    inventory_type = Column(String(100), nullable=True)  # warehouse, classroom, office, etc.
    manager_staff_id = Column(Integer, ForeignKey('staff.id'), nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    manager = relationship("Staff")
    items = relationship("InventoryItem", back_populates="inventory")


class ItemCategory(Base):
    __tablename__ = "item_categories"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent_category_id = Column(Integer, ForeignKey('item_categories.id'), nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    parent = relationship("ItemCategory", remote_side=[id])
    items = relationship("Item", back_populates="category")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    sku = Column(String(100), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('item_categories.id'), nullable=True, index=True)
    
    # Item details
    unit_of_measure = Column(String(50), nullable=False, default="piece")  # piece, kg, liter, etc.
    unit_cost = Column(Numeric(10, 2), nullable=True)
    reorder_level = Column(Integer, nullable=True)  # Minimum stock level
    max_stock_level = Column(Integer, nullable=True)  # Maximum stock level
    
    # Item properties
    is_consumable = Column(Boolean, default=True, nullable=False)
    is_trackable = Column(Boolean, default=True, nullable=False)  # Track individual items
    barcode = Column(String(255), nullable=True)
    
    # Status
    status = Column(String(50), nullable=False, default="active")  # active, inactive, discontinued
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("ItemCategory", back_populates="items")
    inventory_items = relationship("InventoryItem", back_populates="item")
    stock_movements = relationship("StockMovement", back_populates="item")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    inventory_id = Column(Integer, ForeignKey('inventories.id'), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False, index=True)
    
    # Stock levels
    current_stock = Column(Integer, nullable=False, default=0)
    reserved_stock = Column(Integer, nullable=False, default=0)  # Stock allocated but not yet issued
    available_stock = Column(Integer, nullable=False, default=0)  # current_stock - reserved_stock
    
    # Location within inventory
    location_code = Column(String(100), nullable=True)  # Shelf, bin, etc.
    
    # Last updated
    last_counted_at = Column(DateTime(timezone=True), nullable=True)
    last_movement_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    inventory = relationship("Inventory", back_populates="items")
    item = relationship("Item", back_populates="inventory_items")


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False, index=True)
    inventory_id = Column(Integer, ForeignKey('inventories.id'), nullable=False, index=True)
    
    # Movement details
    movement_type = Column(String(50), nullable=False)  # in, out, transfer, adjustment
    quantity = Column(Integer, nullable=False)  # Positive for in, negative for out
    unit_cost = Column(Numeric(10, 2), nullable=True)
    total_cost = Column(Numeric(10, 2), nullable=True)
    
    # References
    reference_type = Column(String(50), nullable=True)  # purchase, sale, transfer, adjustment
    reference_id = Column(Integer, nullable=True)  # ID of related record
    reference_number = Column(String(255), nullable=True)  # External reference
    
    # Movement reason and details
    reason = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Metadata
    moved_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    movement_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    item = relationship("Item", back_populates="stock_movements")
    inventory = relationship("Inventory")
    moved_by_user = relationship("User")


class StockAdjustment(Base):
    __tablename__ = "stock_adjustments"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    inventory_id = Column(Integer, ForeignKey('inventories.id'), nullable=False, index=True)
    adjustment_number = Column(String(100), nullable=False, unique=True)
    
    # Adjustment details
    adjustment_type = Column(String(50), nullable=False)  # physical_count, damage, theft, etc.
    description = Column(Text, nullable=True)
    total_value_change = Column(Numeric(10, 2), nullable=False, default=0)
    
    # Status
    status = Column(String(50), nullable=False, default="draft")  # draft, approved, posted
    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    inventory = relationship("Inventory")
    creator = relationship("User", foreign_keys=[created_by])
    approver = relationship("User", foreign_keys=[approved_by])
    items = relationship("StockAdjustmentItem", back_populates="adjustment", cascade="all, delete-orphan")


class StockAdjustmentItem(Base):
    __tablename__ = "stock_adjustment_items"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    adjustment_id = Column(Integer, ForeignKey('stock_adjustments.id'), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False, index=True)
    
    # Adjustment details
    system_quantity = Column(Integer, nullable=False)  # Quantity according to system
    physical_quantity = Column(Integer, nullable=False)  # Quantity counted physically
    difference = Column(Integer, nullable=False)  # physical_quantity - system_quantity
    unit_cost = Column(Numeric(10, 2), nullable=True)
    value_change = Column(Numeric(10, 2), nullable=False, default=0)
    reason = Column(String(255), nullable=True)

    # Relationships
    adjustment = relationship("StockAdjustment", back_populates="items")
    item = relationship("Item") 