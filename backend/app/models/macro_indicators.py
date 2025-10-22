"""
Macro Economic Indicators Models
Stores data from Eurostat, ECB, IMF, OECD
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class MacroIndicator(Base):
    """
    Generic macro indicator storage
    Supports data from multiple sources (Eurostat, ECB, IMF, OECD)
    """
    __tablename__ = "macro_indicators"

    id = Column(Integer, primary_key=True, index=True)
    
    # Source and classification
    source = Column(String, nullable=False, index=True)  # eurostat, ecb, imf, oecd
    indicator_code = Column(String, nullable=False, index=True)  # GDP, UNEMP, HICP, etc.
    indicator_name = Column(String, nullable=False)
    
    # Geographic and temporal
    country_code = Column(String(3), nullable=False, index=True)  # ISO 3166-1 alpha-3 (NLD, BEL, LUX, DEU)
    period_date = Column(Date, nullable=False, index=True)
    frequency = Column(String(1), nullable=False)  # A=Annual, Q=Quarterly, M=Monthly
    
    # Value and metadata
    value = Column(Float, nullable=True)  # Null if data not available
    unit = Column(String, nullable=True)  # %, EUR, Index, etc.
    is_forecast = Column(String, default=False)  # True for IMF forecasts
    
    # Data quality
    status = Column(String, nullable=True)  # provisional, final, estimated
    data_source_url = Column(String, nullable=True)  # API endpoint used
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_refreshed = Column(DateTime(timezone=True), nullable=True)
    
    # Ensure no duplicates
    __table_args__ = (
        UniqueConstraint('source', 'indicator_code', 'country_code', 'period_date', 
                        name='uix_macro_indicator_unique'),
        Index('idx_macro_country_indicator_date', 'country_code', 'indicator_code', 'period_date'),
        Index('idx_macro_source_country', 'source', 'country_code'),
    )

    def __repr__(self):
        return f"<MacroIndicator {self.source}:{self.indicator_code} {self.country_code} {self.period_date} = {self.value}{self.unit}>"


class InterestRate(Base):
    """
    Interest rates from ECB and national central banks
    Specialized table for financial market rates
    """
    __tablename__ = "interest_rates"

    id = Column(Integer, primary_key=True, index=True)
    
    # Source
    source = Column(String, nullable=False, default='ECB', index=True)
    rate_type = Column(String, nullable=False, index=True)  # DFR, MRO, MLF, ESTR, EURIBOR
    rate_name = Column(String, nullable=False)
    
    # Geographic (EUR for ECB, country-specific for national banks)
    currency = Column(String(3), default='EUR', index=True)
    country_code = Column(String(3), nullable=True)  # Null for ECB rates
    
    # Temporal
    period_date = Column(Date, nullable=False, index=True)
    
    # Value
    rate_value = Column(Float, nullable=False)  # Basis points or percentage
    unit = Column(String, default='%')
    
    # Metadata
    frequency = Column(String(1), default='D')  # D=Daily, W=Weekly, M=Monthly
    data_source_url = Column(String, nullable=True)
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_refreshed = Column(DateTime(timezone=True), nullable=True)
    
    # Ensure no duplicates
    __table_args__ = (
        UniqueConstraint('source', 'rate_type', 'currency', 'period_date', 
                        name='uix_interest_rate_unique'),
        Index('idx_rate_type_date', 'rate_type', 'period_date'),
    )

    def __repr__(self):
        return f"<InterestRate {self.source}:{self.rate_type} {self.period_date} = {self.rate_value}%>"


class EconomicForecast(Base):
    """
    Economic forecasts from IMF, OECD, ECB
    Separate table to distinguish historical vs. forecast data
    """
    __tablename__ = "economic_forecasts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Source
    source = Column(String, nullable=False, index=True)  # IMF_WEO, OECD, ECB_SPF
    forecast_date = Column(Date, nullable=False, index=True)  # When forecast was made
    indicator_code = Column(String, nullable=False, index=True)
    indicator_name = Column(String, nullable=False)
    
    # Geographic and temporal
    country_code = Column(String(3), nullable=False, index=True)
    target_period = Column(Date, nullable=False, index=True)  # Period being forecasted
    frequency = Column(String(1), nullable=False)  # A=Annual, Q=Quarterly
    
    # Forecast value
    forecast_value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    confidence_interval_low = Column(Float, nullable=True)  # Lower bound (if available)
    confidence_interval_high = Column(Float, nullable=True)  # Upper bound (if available)
    
    # Comparison with actual (once available)
    actual_value = Column(Float, nullable=True)  # Filled in once actual data released
    forecast_error = Column(Float, nullable=True)  # actual - forecast
    
    # Metadata
    forecast_horizon = Column(Integer, nullable=True)  # Months ahead (e.g., 12, 24)
    data_source_url = Column(String, nullable=True)
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Ensure no duplicates
    __table_args__ = (
        UniqueConstraint('source', 'forecast_date', 'indicator_code', 'country_code', 'target_period',
                        name='uix_forecast_unique'),
        Index('idx_forecast_country_indicator', 'country_code', 'indicator_code', 'target_period'),
    )

    def __repr__(self):
        return f"<Forecast {self.source}:{self.indicator_code} {self.country_code} {self.target_period} = {self.forecast_value}{self.unit}>"


class DataRefreshLog(Base):
    """
    Logs all data refresh operations for monitoring and debugging
    """
    __tablename__ = "data_refresh_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Source
    source = Column(String, nullable=False, index=True)  # eurostat, ecb, imf, yahoo
    refresh_type = Column(String, nullable=False)  # full, incremental, backfill
    
    # Status
    status = Column(String, nullable=False, index=True)  # started, completed, failed
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Results
    records_processed = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    
    # Error handling
    error_message = Column(String, nullable=True)
    error_details = Column(String, nullable=True)  # Stack trace if failed
    
    # Metadata
    trigger = Column(String, nullable=True)  # manual, scheduled, api_request
    triggered_by = Column(String, nullable=True)  # user_id or system
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<DataRefreshLog {self.source} {self.status} {self.started_at}>"


class MarketData(Base):
    """
    Market data from Yahoo Finance (stocks, indices, currencies)
    Optimized for time-series queries
    """
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    
    # Security identification
    ticker = Column(String, nullable=False, index=True)  # ASML.AS, ^AEX, EURUSD=X
    security_type = Column(String, nullable=False)  # stock, index, currency, etf
    security_name = Column(String, nullable=True)
    exchange = Column(String, nullable=True)  # AMS, XETRA, FX
    
    # Temporal
    date = Column(Date, nullable=False, index=True)
    
    # OHLCV data
    open_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    low_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=False)  # Most important
    volume = Column(Float, nullable=True)
    
    # Additional metrics
    adjusted_close = Column(Float, nullable=True)  # Adjusted for splits/dividends
    market_cap = Column(Float, nullable=True)  # For stocks
    
    # Metadata
    currency = Column(String(3), default='EUR')
    data_source = Column(String, default='yahoo_finance')
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_refreshed = Column(DateTime(timezone=True), nullable=True)
    
    # Ensure no duplicates
    __table_args__ = (
        UniqueConstraint('ticker', 'date', name='uix_market_data_unique'),
        Index('idx_market_ticker_date', 'ticker', 'date'),
        Index('idx_market_type_date', 'security_type', 'date'),
    )

    def __repr__(self):
        return f"<MarketData {self.ticker} {self.date} close={self.close_price}>"
