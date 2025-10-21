"""
Data source and fetch log models
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DataSource(Base):
    """Configuration and metadata for external data sources"""
    
    __tablename__ = "data_sources"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Identification
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # eurostat, ecb, worldbank, oecd
    
    # Configuration
    api_base_url: Mapped[str] = mapped_column(String(500), nullable=False)
    api_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_healthy: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    documentation_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Statistics
    total_fetches: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    successful_fetches: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failed_fetches: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_fetch_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_success_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    __table_args__ = (
        Index('ix_data_sources_active', 'is_active'),
        Index('ix_data_sources_type', 'source_type'),
    )
    
    def __repr__(self) -> str:
        return f"<DataSource(name='{self.name}', type='{self.source_type}', active={self.is_active})>"
    
    def to_dict(self) -> dict:
        """Convert data source to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "source_type": self.source_type,
            "is_active": self.is_active,
            "is_healthy": self.is_healthy,
            "total_fetches": self.total_fetches,
            "successful_fetches": self.successful_fetches,
            "failed_fetches": self.failed_fetches,
            "last_fetch_at": self.last_fetch_at.isoformat() if self.last_fetch_at else None,
            "last_success_at": self.last_success_at.isoformat() if self.last_success_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class FetchLog(Base):
    """Detailed logs of data fetch operations"""
    
    __tablename__ = "fetch_logs"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Source identification
    source_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    dataset: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Execution details
    status: Mapped[str] = mapped_column(String(20), index=True, nullable=False)  # success, error, partial
    records_fetched: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_stored: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_skipped: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Performance
    duration_seconds: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Error handling
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Additional context
    fetch_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Timestamp
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    
    __table_args__ = (
        Index('ix_fetch_logs_source_date', 'source_name', 'completed_at'),
        Index('ix_fetch_logs_status', 'status'),
        Index('ix_fetch_logs_completed_at', 'completed_at'),
    )
    
    def __repr__(self) -> str:
        return (
            f"<FetchLog("
            f"source='{self.source_name}', "
            f"status='{self.status}', "
            f"records={self.records_stored}"
            f")>"
        )
    
    def to_dict(self) -> dict:
        """Convert fetch log to dictionary"""
        return {
            "id": self.id,
            "source_name": self.source_name,
            "dataset": self.dataset,
            "status": self.status,
            "records_fetched": self.records_fetched,
            "records_stored": self.records_stored,
            "records_skipped": self.records_skipped,
            "duration_seconds": self.duration_seconds,
            "error_message": self.error_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
