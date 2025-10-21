"""
Export model for tracking generated files
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Export(Base):
    """Tracks generated export files (CSV, Excel, PDF)"""
    
    __tablename__ = "exports"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # User reference
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    
    # Export details
    export_type: Mapped[str] = mapped_column(String(20), nullable=False)  # csv, excel, pdf
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Query parameters used for export
    query_params: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)  # pending, completed, failed, expired
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    row_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    column_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    downloaded_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    __table_args__ = (
        Index('ix_exports_user_created', 'user_id', 'created_at'),
        Index('ix_exports_status', 'status'),
        Index('ix_exports_expires_at', 'expires_at'),
    )
    
    def __repr__(self) -> str:
        return (
            f"<Export("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"type='{self.export_type}', "
            f"status='{self.status}'"
            f")>"
        )
    
    def to_dict(self) -> dict:
        """Convert export to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "export_type": self.export_type,
            "filename": self.filename,
            "file_size_bytes": self.file_size_bytes,
            "status": self.status,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "downloaded_at": self.downloaded_at.isoformat() if self.downloaded_at else None,
        }
    
    def is_expired(self) -> bool:
        """Check if export has expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
