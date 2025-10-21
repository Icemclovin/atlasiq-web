"""
Indicator value model for time-series macro data
"""
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Date, DateTime, Float, String, Text, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class IndicatorValue(Base):
    """Time-series indicator values for countries and sectors"""
    
    __tablename__ = "indicator_values"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Dimensions
    country_code: Mapped[str] = mapped_column(String(10), index=True, nullable=False)
    sector: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    indicator_code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    
    # Time dimension
    date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    period_type: Mapped[str] = mapped_column(
        String(20),
        default="monthly",
        nullable=False
    )  # monthly, quarterly, annual
    
    # Value
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Metadata
    source: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    source_dataset: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    indicator_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    indicator_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Additional metadata as JSON
    extra_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Quality flags
    is_estimated: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_provisional: Mapped[bool] = mapped_column(default=False, nullable=False)
    quality_flag: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    
    # Timestamps
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    
    # Composite indexes for common queries
    __table_args__ = (
        # Query by country + indicator + date range
        Index('ix_indicator_country_code_date', 'country_code', 'indicator_code', 'date'),
        # Query by sector + indicator
        Index('ix_indicator_sector_code', 'sector', 'indicator_code'),
        # Query by source
        Index('ix_indicator_source_date', 'source', 'date'),
        # Time-series queries
        Index('ix_indicator_date_desc', 'date', postgresql_using='btree'),
        # Composite unique constraint
        Index(
            'uq_indicator_country_sector_code_date',
            'country_code', 'sector', 'indicator_code', 'date',
            unique=True
        ),
    )
    
    def __repr__(self) -> str:
        return (
            f"<IndicatorValue("
            f"country={self.country_code}, "
            f"indicator={self.indicator_code}, "
            f"date={self.date}, "
            f"value={self.value}"
            f")>"
        )
    
    def to_dict(self) -> dict:
        """Convert indicator to dictionary"""
        return {
            "id": self.id,
            "country_code": self.country_code,
            "sector": self.sector,
            "indicator_code": self.indicator_code,
            "indicator_name": self.indicator_name,
            "date": self.date.isoformat() if self.date else None,
            "period_type": self.period_type,
            "value": self.value,
            "unit": self.unit,
            "source": self.source,
            "source_dataset": self.source_dataset,
            "extra_metadata": self.extra_metadata,
            "is_estimated": self.is_estimated,
            "is_provisional": self.is_provisional,
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
        }
