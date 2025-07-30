"""Formatting utilities for the Lightwave ecosystem."""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Union


def format_currency(
    amount: Union[int, float, Decimal, None], 
    currency: str = "USD",
    locale: str = "en_US"
) -> Optional[str]:
    """Format a monetary amount as currency.
    
    Args:
        amount: The monetary amount to format (or None)
        currency: Currency code (e.g., 'USD', 'EUR')
        locale: Locale for formatting (e.g., 'en_US', 'de_DE')
        
    Returns:
        Formatted currency string or None if amount is None
        
    Examples:
        >>> format_currency(1234.56)
        '$1,234.56'
        >>> format_currency(1234.56, 'EUR')
        '$1,234.56 EUR'
    """
    if amount is None:
        return None
    
    # Convert to Decimal for precise handling
    if isinstance(amount, (int, float)):
        amount = Decimal(str(amount))
    
    # Format with thousands separator and USD symbol
    formatted = f"${amount:,.2f}"
    
    # Add currency code if not USD
    if currency != "USD":
        formatted += f" {currency}"
    
    return formatted


def format_date(
    date: Union[datetime, str, None],
    format_str: Optional[str] = None
) -> Optional[str]:
    """Format a date according to the given format string.
    
    Args:
        date: Date to format (datetime object, ISO string, or None)
        format_str: strftime format string (defaults to ISO date format)
        
    Returns:
        Formatted date string or None if date is None/invalid
        
    Examples:
        >>> from datetime import datetime
        >>> dt = datetime(2023, 1, 15, 12, 30, 45)
        >>> format_date(dt)
        '2023-01-15'
        >>> format_date(dt, '%m/%d/%Y')
        '01/15/2023'
    """
    if date is None:
        return None
    
    # Convert string to datetime if needed
    if isinstance(date, str):
        try:
            if date.endswith('Z'):
                date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            else:
                date = datetime.fromisoformat(date)
        except ValueError:
            return None  # Return None for invalid date strings
    
    if not isinstance(date, datetime):
        return None
    
    # Use default ISO date format if no format string provided
    if format_str is None:
        return date.date().isoformat()
    
    # Use the provided format string
    try:
        return date.strftime(format_str)
    except ValueError:
        return None


def format_duration(seconds: Union[int, float]) -> str:
    """Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
        
    Examples:
        >>> format_duration(3661)
        '1h 1m 1s'
        >>> format_duration(90)
        '1m 30s'
    """
    if seconds < 0:
        return "0s"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
        
    Examples:
        >>> format_file_size(1024)
        '1.0 KB'
        >>> format_file_size(1536)
        '1.5 KB'
    """
    if size_bytes < 0:
        return "0 B"
    
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    
    for i, unit in enumerate(units):
        size = size_bytes / (1024 ** i)
        if size < 1024 or i == len(units) - 1:
            if i == 0:
                return f"{int(size)} {unit}"
            else:
                return f"{size:.1f} {unit}"
    
    return f"{size_bytes} B"