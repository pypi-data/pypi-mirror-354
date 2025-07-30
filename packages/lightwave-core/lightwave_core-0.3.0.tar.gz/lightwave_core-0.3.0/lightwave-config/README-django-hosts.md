# Django Hosts for Lightwave Ecosystem

This document explains how to implement and configure Django Hosts for subdomain routing in Lightwave applications.

## Overview

The Lightwave ecosystem uses a multi-subdomain architecture following these patterns:

- `admin.domain.tld` - System administration and CMS
- `auth.domain.tld` - Authentication service
- `api.domain.tld` - API endpoints
- `app.domain.tld` - Main web application
- `cdn.domain.tld` - Asset delivery
- `mobile.domain.tld` - Mobile app API (optional)
- `desktop.domain.tld` - Desktop app API (optional)

We use [django-hosts](https://github.com/jazzband/django-hosts) to implement subdomain routing in a standardized way across all Lightwave applications.

## Configuration Files

This package provides several configuration files to set up django-hosts:

1. `django-hosts-config.yaml` - Configuration for all subdomains and applications
2. `django-settings-hosts.py` - Helper functions to configure Django settings
3. `hosts.py` - Django Hosts pattern definition (in the lightwave_core package)

## Installation

1. Install django-hosts in your environment:

```bash
uv pip install django-hosts
```

2.Import the settings configuration in your Django project's settings.py:

```python
# Add to your project's settings.py

# Import django-hosts settings
from lightwave_config.django_settings_hosts import configure_hosts_settings

# Configure django-hosts
configure_hosts_settings(sys.modules[__name__])

# Alternatively, set individual settings:
ROOT_HOSTCONF = 'lightwave.core.hosts'
DEFAULT_HOST = 'app'  # or whichever is your default
PARENT_HOST = 'example.com'  # Your domain name