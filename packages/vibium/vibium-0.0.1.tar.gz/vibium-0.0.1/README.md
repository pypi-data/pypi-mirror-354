# Vibium

A minimal AI interface for UI automation.

## Installation

```bash
pip install vibium
```

## Usage

```python
from vibium import Vibium

vibe = Vibium(device='iphone')
vibe.do("open pinthing.com")
vibe.check("do you see a clock?")
vibe.check("does the time match the current time?")
```
