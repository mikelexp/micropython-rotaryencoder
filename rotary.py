# MicroPython Rotary Encoder Library
# IRQ-based quadrature rotary encoder driver for RP2040 / MicroPython.
#
# MIT License
# Copyright (c) 2024 Miguel Scaramozzino

from machine import Pin


class RotaryIRQ:
    """
    IRQ-based quadrature rotary encoder driver for MicroPython (RP2040).

    Uses a quadrature state-transition table to filter mechanical bounce,
    so no additional debounce delay is needed.

    Parameters
    ----------
    pin_num_clk : int  — GPIO number for the CLK (A) pin
    pin_num_dt  : int  — GPIO number for the DT (B) pin
    reverse     : bool — if True, reverses the count direction (default False)
    divisor     : int  — number of IRQ transitions per physical detent (default 4)
    """

    def __init__(self, pin_num_clk, pin_num_dt, reverse=False, divisor=4):
        self._pin_clk = Pin(pin_num_clk, Pin.IN, Pin.PULL_UP)
        self._pin_dt = Pin(pin_num_dt, Pin.IN, Pin.PULL_UP)
        self._reverse = -1 if reverse else 1
        self._divisor = divisor
        self._raw_value = 0

        # Initial state (bit1: CLK, bit0: DT)
        self._state = (self._pin_clk.value() << 1) | self._pin_dt.value()

        # Attach IRQs on both pins, both edges
        self._pin_clk.irq(handler=self._process, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)
        self._pin_dt.irq(handler=self._process, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

    def _process(self, pin):
        new_state = (self._pin_clk.value() << 1) | self._pin_dt.value()
        if new_state != self._state:
            # Valid quadrature transition table
            transition = (self._state << 2) | new_state
            if transition in (0b0010, 0b1011, 0b1101, 0b0100):
                self._raw_value += self._reverse
            elif transition in (0b0001, 0b0111, 0b1110, 0b1000):
                self._raw_value -= self._reverse
            self._state = new_state

    def value(self):
        """Return the encoder position adjusted by the divisor (physical detents)."""
        return self._raw_value // self._divisor

    def set(self, val):
        """Set the current encoder position (adjusted by the divisor)."""
        self._raw_value = val * self._divisor
