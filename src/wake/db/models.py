"""Database models"""

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Table, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class DistributionCenter(Base):
    __tablename__ = "distribution_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    zip_code = Column(Integer, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_product_id = Column(Integer, nullable=True)
    parent_name = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    variants = relationship("ProductVariant", back_populates="product")
    info = relationship("ProductInfo", back_populates="product")


class ProductVariant(Base):
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    sku = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    ean = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    is_valid = Column(Boolean, default=True, nullable=False)
    show_on_site = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    product = relationship("Product", back_populates="variants")
    pricing = relationship("VariantPricing", back_populates="variant", uselist=False)
    stock = relationship("VariantStock", back_populates="variant")
    attributes = relationship("VariantAttribute", back_populates="variant")


class VariantPricing(Base):
    __tablename__ = "variant_pricing"
    
    variant_id = Column(Integer, ForeignKey("product_variants.id"), primary_key=True)
    cost_price = Column(Float, nullable=True)
    original_price = Column(Float, nullable=True)
    sale_price = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    variant = relationship("ProductVariant", back_populates="pricing")


class VariantAttribute(Base):
    __tablename__ = "variant_attributes"
    
    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)
    attribute_type = Column(String, nullable=False)  # e.g., "Selecao"
    name = Column(String, nullable=False)  # e.g., "Tamanho", "Cor"
    value = Column(String, nullable=False)  # e.g., "P", "PRETO"
    is_filter = Column(Boolean, default=False, nullable=False)
    display = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    variant = relationship("ProductVariant", back_populates="attributes")
    
    # Indexes for better search performance
    __table_args__ = (
        Index('idx_variant_attributes_variant_id', 'variant_id'),
        Index('idx_variant_attributes_name_value', 'name', 'value'),
    )


class ProductInfo(Base):
    __tablename__ = "product_info"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    info_id = Column(Integer, nullable=False)  # informacaoId from API
    title = Column(String, nullable=False)  # titulo
    text = Column(String, nullable=False)  # texto (can be HTML)
    info_type = Column(String, nullable=False)  # tipoInformacao
    show_on_site = Column(Boolean, default=True, nullable=False)  # exibirSite
    
    # Relationships
    product = relationship("Product", back_populates="info")
    
    # Indexes
    __table_args__ = (
        Index('idx_product_info_product_id', 'product_id'),
        Index('idx_product_info_type', 'info_type'),
    )


class VariantStock(Base):
    __tablename__ = "variant_stock"
    
    variant_id = Column(Integer, ForeignKey("product_variants.id"), primary_key=True)
    distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"), primary_key=True)
    physical_stock = Column(Integer, default=0, nullable=False)
    reserved_stock = Column(Integer, default=0, nullable=False)
    is_available = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    variant = relationship("ProductVariant", back_populates="stock")
    distribution_center = relationship("DistributionCenter")


# Many-to-many relationship table
product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Self-referential relationship
    parent = relationship("Category", remote_side=[id])


class SyncState(Base):
    __tablename__ = "sync_state"
    
    id = Column(Integer, primary_key=True, index=True)
    sync_type = Column(String, nullable=False, unique=True)  # 'products', 'categories', etc.
    last_page = Column(Integer, default=0, nullable=False)
    last_sku = Column(String, nullable=True)
    total_synced = Column(Integer, default=0, nullable=False)
    status = Column(String, default="idle", nullable=False)  # 'idle', 'running', 'completed', 'failed'
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)
    extra_data = Column(String, nullable=True)  # JSON string for additional data


class CustomerToken(Base):
    __tablename__ = "customer_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    token = Column(String, nullable=False)
    token_type = Column(String(50), nullable=True)
    valid_until = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)