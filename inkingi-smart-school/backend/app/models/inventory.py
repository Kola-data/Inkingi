from sqlalchemy import Column, String, Float, ForeignKey, Integer, Date, Text, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TenantModel
import enum


class ItemStatus(str, enum.Enum):
    ACTIVE = "active"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class MovementType(str, enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"
    DAMAGE = "damage"
    RETURN = "return"


class Warehouse(TenantModel):
    __tablename__ = "warehouses"
    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_warehouse_name"),
    )
    
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=True)
    is_active = Column(String, default="true", nullable=False)
    
    # Relationships
    items = relationship("InventoryItem", back_populates="warehouse")
    
    def __repr__(self):
        return f"<Warehouse {self.name}>"


class InventoryCategory(TenantModel):
    __tablename__ = "inventory_categories"
    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_inventory_category_name"),
    )
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("inventory_categories.id"), nullable=True)
    
    # Relationships
    items = relationship("InventoryItem", back_populates="category")
    
    def __repr__(self):
        return f"<InventoryCategory {self.name}>"


class InventoryItem(TenantModel):
    __tablename__ = "inventory_items"
    __table_args__ = (
        UniqueConstraint("school_id", "sku", name="uq_inventory_sku"),
    )
    
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("inventory_categories.id"), nullable=True)
    
    sku = Column(String(50), nullable=False)  # Stock Keeping Unit
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Quantities
    quantity_available = Column(Integer, default=0, nullable=False)
    quantity_reserved = Column(Integer, default=0, nullable=False)
    minimum_stock = Column(Integer, default=0, nullable=False)
    maximum_stock = Column(Integer, nullable=True)
    
    # Pricing
    unit_price = Column(Float, nullable=True)
    purchase_price = Column(Float, nullable=True)
    
    # Details
    unit_of_measure = Column(String(20), nullable=True)  # e.g., "pieces", "kg", "liters"
    barcode = Column(String(100), nullable=True)
    manufacturer = Column(String(100), nullable=True)
    supplier = Column(String(100), nullable=True)
    
    status = Column(SQLEnum(ItemStatus), default=ItemStatus.ACTIVE, nullable=False)
    expiry_date = Column(Date, nullable=True)
    
    # Relationships
    warehouse = relationship("Warehouse", back_populates="items")
    category = relationship("InventoryCategory", back_populates="items")
    movements = relationship("StockMovement", back_populates="item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<InventoryItem {self.sku} - {self.name}>"


class StockMovement(TenantModel):
    __tablename__ = "stock_movements"
    
    item_id = Column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=False)
    movement_type = Column(SQLEnum(MovementType), nullable=False)
    
    quantity = Column(Integer, nullable=False)  # Positive for IN, negative for OUT
    unit_price = Column(Float, nullable=True)
    total_value = Column(Float, nullable=True)
    
    # Movement details
    reference_number = Column(String(100), nullable=True)
    from_warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=True)
    to_warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=True)
    
    movement_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    
    # Tracking
    performed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Stock levels after movement
    quantity_before = Column(Integer, nullable=False)
    quantity_after = Column(Integer, nullable=False)
    
    # Relationships
    item = relationship("InventoryItem", back_populates="movements")
    
    def __repr__(self):
        return f"<StockMovement {self.item_id} - {self.movement_type} ({self.quantity})>"