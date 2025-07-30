"""Base model class for all Lightwave models."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field


class BaseModel(PydanticBaseModel):
    """Base model class with common functionality for all Lightwave models.
    
    Provides:
    - Consistent configuration across all models
    - API serialization/deserialization methods
    - Common timestamp fields
    - Type safety and validation
    """
    
    model_config = ConfigDict(
        extra="forbid",  # Prevent extra fields
        validate_assignment=True,  # Validate on assignment
        use_enum_values=True,  # Use enum values in serialization
        arbitrary_types_allowed=True  # Allow custom types
    )
    
    # Common timestamp fields (optional for flexibility)
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    
    def dict_for_api(self) -> Dict[str, Any]:
        """Convert model to dictionary suitable for API responses.
        
        Returns:
            Dictionary representation with proper serialization for API.
        """
        data = self.model_dump(
            mode="python",  # Use python mode to keep datetime objects
            exclude_none=False,  # Include None values for API consistency
            by_alias=True
        )
        return data
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "BaseModel":
        """Create model instance from API response data.
        
        Args:
            data: Dictionary data from API response
            
        Returns:
            Model instance created from the data
        """
        # Handle datetime strings from API
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
            
        return cls(**data)
    
    def update_timestamps(self) -> None:
        """Update the timestamps for this model."""
        now = datetime.utcnow()
        if self.created_at is None:
            self.created_at = now
        self.updated_at = now