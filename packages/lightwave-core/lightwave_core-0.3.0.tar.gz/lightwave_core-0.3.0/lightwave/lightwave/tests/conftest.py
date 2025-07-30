"""Common test fixtures for LightWave AI Services."""

import os
import asyncio
from typing import Any, Dict, Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from lightwave_ai.main import app as fastapi_app
from lightwave_ai.config import Settings, settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for tests.
    
    Returns:
        Event loop
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings() -> Settings:
    """Get test settings.
    
    Returns:
        Test settings
    """
    # Override settings for testing
    test_settings = Settings(
        ENV="testing",
        DEBUG=True,
        API_KEY="test-api-key",
        DATABASE_URL="postgresql://postgres:postgres@localhost:5432/lightwave_test",
        OPENAI_API_KEY="test-openai-key",
        ANTHROPIC_API_KEY="test-anthropic-key",
    )
    
    return test_settings


@pytest.fixture
async def app(test_settings: Settings) -> FastAPI:
    """Get the FastAPI app for testing.
    
    Args:
        test_settings: Test settings
        
    Returns:
        FastAPI app
    """
    # Override settings with test settings
    for key, value in test_settings.dict().items():
        setattr(settings, key, value)
    
    return fastapi_app


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    """Get an async client for testing.
    
    Args:
        app: FastAPI app
        
    Returns:
        Async client
    """
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://test",
            headers={"X-API-Key": "test-api-key"},
        ) as client:
            yield client 