"""
Light Sensor utility module for BH1750 sensors

This module provides utilities for working with BH1750 light sensors,
including single sensor and multi-sensor (with I2C multiplexer) configurations.

Classes:
    LightSensor: Single BH1750 light sensor management

Example:
    >>> from big_thing_py.utils.light_sensor import LightSensor
    >>> import board
    >>> sensor = LightSensor(board.I2C())
    >>> print(f"Light level: {sensor.lux} lux")
"""

from .light_sensor import LightSensor

__all__ = ['LightSensor']
