#!/usr/bin/env python
"""
Start up an instrument server and load drivers.
"""
from pathlib import Path

from nspyre import start_instrument_server

HERE = Path(__file__).parent

start_instrument_server(drivers=[
    {
        'name': 'drv3',
        'class_path': HERE / 'drivers' / 'driver.py',
        'class_name': 'FakeODMRInstrument',
        'args': [],
        'kwargs': {}
    }],
    inserv_kwargs={
        'port': 42067
    }
)
