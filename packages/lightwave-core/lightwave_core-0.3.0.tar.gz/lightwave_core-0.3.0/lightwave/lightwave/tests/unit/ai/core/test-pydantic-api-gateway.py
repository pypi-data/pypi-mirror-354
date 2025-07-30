#!/usr/bin/env python3
"""
Test client for the Figma-to-React PydanticAI service through the API gateway.
This demonstrates advanced PydanticAI tool features.
"""

import asyncio
import json
import os
from typing import Dict, Any, List, Optional, Union
import httpx
from enum import Enum
from pydantic import BaseModel, Field


# API Gateway URL
API_GATEWAY_URL = os.environ.get("API_GATEWAY_URL", "http://localhost:8002")
FIGMA_TO_REACT_ENDPOINT = f"{API_GATEWAY_URL}/api/ai/figma-react/convert"


class FigmaComponentType(str, Enum):
    """Type of Figma component to convert."""
    BUTTON = "button"
    CARD = "card"
    FORM = "form"
    NAVIGATION = "navigation"
    MODAL = "modal"
    TABLE = "table"
    LIST = "list"
    CUSTOM = "custom"


class ComponentRequest(BaseModel):
    """Request model for component conversion."""
    figma_file_url: str
    component_name: str
    component_type: FigmaComponentType
    include_styles: bool = True
    react_version: str = "18"
    style_framework: str = "css"
    typescript: bool = False
    access_token: Optional[str] = None
    additional_notes: Optional[str] = None


async def convert_component(request: ComponentRequest) -> Dict[str, Any]:
    """
    Send a component conversion request to the API gateway.
    
    Args:
        request: Component conversion request
        
    Returns:
        Conversion response
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            FIGMA_TO_REACT_ENDPOINT,
            json=request.dict(),
            timeout=60.0,  # Increased timeout for LLM processing
        )
        
        if response.status_code != 200:
            error_detail = "Unknown error"
            try:
                error_data = response.json()
                error_detail = error_data.get("detail", error_detail)
            except Exception:
                pass
            raise Exception(f"API error: {response.status_code} - {error_detail}")
        
        return response.json()


async def demo_button_component():
    """Demonstrate converting a Button component."""
    print("\n=== Button Component Demo ===\n")
    
    # Create a request for a Button component
    request = ComponentRequest(
        figma_file_url="https://www.figma.com/file/example123/UI-Components",
        component_name="Button",
        component_type=FigmaComponentType.BUTTON,
        style_framework="styled-components",
        typescript=True
    )
    
    print(f"Converting {request.component_name} component...")
    
    try:
        result = await convert_component(request)
        
        # Display the first component
        if "components" in result and len(result["components"]) > 0:
            component = result["components"][0]
            print(f"\nComponent: {component.get('name')}")
            
            print("\nProps:")
            for prop in component.get("props", []):
                required = "required" if prop.get("required") else "optional"
                default = f", default: {prop.get('default_value')}" if prop.get("default_value") is not None else ""
                print(f"- {prop.get('name')}: {prop.get('type')} ({required}{default})")
                if prop.get("description"):
                    print(f"  Description: {prop.get('description')}")
            
            print("\nDependencies:")
            for dep in component.get("dependencies", []):
                print(f"- {dep}")
            
            print("\nCode (first 10 lines):")
            code_lines = component.get("jsx_code", "").split("\n")
            for line in code_lines[:10]:
                print(line)
            print("...")
            
            if component.get("css_code"):
                print("\nCSS (first 5 lines):")
                css_lines = component.get("css_code", "").split("\n")
                for line in css_lines[:5]:
                    print(line)
                print("...")
            
            print("\nUsage Example (first 5 lines):")
            example_lines = component.get("usage_example", "").split("\n")
            for line in example_lines[:5]:
                print(line)
            print("...")
            
        if "suggestions" in result and len(result["suggestions"]) > 0:
            print("\nSuggestions:")
            for suggestion in result["suggestions"]:
                print(f"- {suggestion}")
    
    except Exception as e:
        print(f"\nError: {e}")


async def demo_card_component():
    """Demonstrate converting a Card component."""
    print("\n=== Card Component Demo ===\n")
    
    # Create a request for a Card component
    request = ComponentRequest(
        figma_file_url="https://www.figma.com/file/example123/UI-Components",
        component_name="Card",
        component_type=FigmaComponentType.CARD,
        style_framework="tailwind",
        typescript=True,
        additional_notes="Make it responsive with support for dark mode"
    )
    
    print(f"Converting {request.component_name} component...")
    
    try:
        result = await convert_component(request)
        
        # Display basic info
        if "components" in result and len(result["components"]) > 0:
            component = result["components"][0]
            print(f"\nComponent: {component.get('name')}")
            
            print(f"\nCode file would be: {component.get('name')}.{('tsx' if request.typescript else 'jsx')}")
            
            print("\nProps count:", len(component.get("props", [])))
            print("Dependencies:", ", ".join(component.get("dependencies", [])))
            
            if component.get("css_code"):
                print(f"\nCSS file would be: {component.get('name')}.css")
            
    except Exception as e:
        print(f"\nError: {e}")


async def main():
    """Run the demonstration."""
    print("\n=== Figma-to-React PydanticAI Service Demo ===\n")
    print(f"API Gateway URL: {API_GATEWAY_URL}")
    print(f"Endpoint: {FIGMA_TO_REACT_ENDPOINT}")
    
    # Check if the service is available
    try:
        async with httpx.AsyncClient() as client:
            health_response = await client.get(f"{API_GATEWAY_URL}/api/ai/health")
            figma_react_status = "Unknown"
            
            if health_response.status_code == 200:
                health_data = health_response.json()
                figma_react_status = health_data.get("figma_to_react", {}).get("status", "Unknown")
            
            print(f"Figma-to-React Service Status: {figma_react_status}")
            
            if figma_react_status != "ok":
                print("\nWarning: Figma-to-React service may not be available.")
                print("Make sure you've started the service with: ./run-pydantic-figma-react.sh")
                user_input = input("\nDo you want to continue anyway? (y/n): ")
                if user_input.lower() != "y":
                    print("Exiting...")
                    return
    except Exception as e:
        print(f"\nWarning: Could not check service health: {e}")
        user_input = input("\nDo you want to continue anyway? (y/n): ")
        if user_input.lower() != "y":
            print("Exiting...")
            return
    
    await demo_button_component()
    await demo_card_component()


if __name__ == "__main__":
    asyncio.run(main()) 