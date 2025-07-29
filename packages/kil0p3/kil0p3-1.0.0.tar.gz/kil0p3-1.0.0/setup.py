#!/usr/bin/env python3
"""
setup.py для публикации kil0p3 на PyPI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Читаем README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else """
# Kil0p3 - Advanced Python Application Protection

🔐 **Automatic protection activation on import**

```python
import kil0p3  # Protection starts automatically!
```

## Features
- License validation with digital signatures
- Hardware ID (HWID) binding
- Anti-debugging protection
- Code integrity verification
- Automatic blocking on violations
- Development mode for testing

## Quick Start

### For Development:
```python
import os
os.environ['KIL0P3_DEV_MODE'] = '1'  # Disable protection for development
import kil0p3
```

### For Production:
```python
import kil0p3  # Full protection automatically enabled
```

## License Management

```python
import kil0p3

# Check current status
print(f"Version: {kil0p3.get_version()}")
print(f"Protected: {kil0p3.is_protected()}")
print(f"HWID: {kil0p3.get_hwid()}")

# Set license programmatically
kil0p3.set_license("KLP-XXXX-XXXX-XXXX-XXXX")
```

Visit [GitHub](https://github.com/kil0p3-security/kil0p3) for full documentation.
"""

setup(
    name="kil0p3",
    version="1.0.0",
    author="Kil0p3 Security Team",
    author_email="security@kil0p3.dev",
    description="Advanced Python Application Protection Library with automatic license validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kil0p3-security/kil0p3",
    project_urls={
        "Bug Reports": "https://github.com/kil0p3-security/kil0p3/issues",
        "Source": "https://github.com/kil0p3-security/kil0p3",
        "Documentation": "https://kil0p3.dev/docs",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux", 
        "Operating System :: MacOS",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pycryptodome>=3.19.0",
        "cryptography>=41.0.0",
        "requests>=2.31.0", 
        "psutil>=5.9.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0", 
            "isort>=5.0.0",
        ],
        "full": [
            "colorlog>=6.7.0",
            "pytz>=2023.3",
        ]
    },
    include_package_data=True,
    package_data={
        "Kil0p3": [
            "config/*.py",
            "**/*.py",
        ]
    },
    zip_safe=False,
    keywords=[
        "security", "protection", "license", "drm", "anti-piracy", 
        "hardware-id", "hwid", "anti-debugging", "code-protection",
        "license-validation", "software-protection"
    ],
    entry_points={
        "console_scripts": [
            "kil0p3-info=Kil0p3.tools.info:main",
        ],
    },
)