"""Tests for the BaseModel class."""

from datetime import datetime

import pytest
from pydantic import Field

from lightwave.core.models.base import BaseModel


class TestBaseModel:
    """Tests for the BaseModel class."""

    class SampleModel(BaseModel):
        """Sample model for testing BaseModel functionality."""

        name: str
        description: str | None = None
        count: int = Field(default=0)

    def test_model_init(self):
        """Test model initialization."""
        # Test with required fields only
        model = self.SampleModel(name="test")
        assert model.name == "test"
        assert model.description is None
        assert model.count == 0
        assert model.created_at is None
        assert model.updated_at is None

        # Test with all fields
        now = datetime.now()
        model = self.SampleModel(
            name="test",
            description="desc",
            count=5,
            created_at=now,
            updated_at=now,
        )
        assert model.name == "test"
        assert model.description == "desc"
        assert model.count == 5
        assert model.created_at == now
        assert model.updated_at == now

    def test_model_config(self):
        """Test model configuration."""
        # Test extra=forbid
        with pytest.raises(ValueError):
            self.SampleModel(name="test", extra_field="value")

    def test_dict_for_api(self):
        """Test conversion to API dict."""
        model = self.SampleModel(name="test", description="desc", count=5)
        api_dict = model.dict_for_api()

        assert isinstance(api_dict, dict)
        assert api_dict["name"] == "test"
        assert api_dict["description"] == "desc"
        assert api_dict["count"] == 5

        # The existing implementation doesn't include None values
        # But with values set, they should be included
        now = datetime.now()
        model = self.SampleModel(
            name="test",
            description="desc",
            count=5,
            created_at=now,
            updated_at=now,
        )
        api_dict = model.dict_for_api()

        assert "created_at" in api_dict
        assert "updated_at" in api_dict
        assert api_dict["created_at"] == now
        assert api_dict["updated_at"] == now

    def test_from_api_response(self):
        """Test creating model from API response."""
        now = datetime.now()
        data = {
            "name": "test",
            "description": "desc",
            "count": 5,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }

        model = self.SampleModel.from_api_response(data)

        assert model.name == "test"
        assert model.description == "desc"
        assert model.count == 5
        assert isinstance(model.created_at, datetime)
        assert isinstance(model.updated_at, datetime)
