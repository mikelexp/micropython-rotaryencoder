# MicroPython RotaryEncoder

An IRQ-based quadrature rotary encoder driver for MicroPython (RP2040 / Raspberry Pi Pico).

Uses a quadrature state-transition table to filter mechanical bounce — no debounce delay needed.

## Features

- **IRQ-driven**: Zero CPU cost while idle; transitions are caught instantly via pin interrupts.
- **Bounce filtering**: Quadrature state-machine rejects invalid transitions caused by mechanical noise.
- **Direction reversal**: `reverse=True` swaps CW/CCW without rewiring.
- **Configurable divisor**: Adjusts counts-per-detent to match your encoder's resolution (default 4 for typical 20-PPR encoders with 5 detents/cycle).

## Installation

### Using mip (MicroPython 1.19.1+)

```python
import mip
mip.install("github:mikelexp/micropython-rotaryencoder")
```

Or manually copy `rotary.py` to the `lib/` folder on your device.

## Quick Start

```python
from rotary import RotaryIRQ
import time

enc = RotaryIRQ(pin_num_clk=3, pin_num_dt=4)

last = enc.value()
while True:
    v = enc.value()
    if v != last:
        print("Position:", v)
        last = v
    time.sleep_ms(10)
```

## API Reference

### `RotaryIRQ(pin_num_clk, pin_num_dt, reverse=False, divisor=4)`

| Parameter     | Type | Default | Description |
|---------------|------|---------|-------------|
| `pin_num_clk` | int  | —       | GPIO number for CLK (A) pin |
| `pin_num_dt`  | int  | —       | GPIO number for DT (B) pin |
| `reverse`     | bool | `False` | Reverse counting direction |
| `divisor`     | int  | `4`     | IRQ transitions per physical detent |

Both pins are configured as inputs with internal pull-ups. IRQs are attached on rising and falling edges of both pins automatically.

### Methods

- **`value() → int`** — Returns the current encoder position in detents.
- **`set(val: int)`** — Sets the current position to `val` detents.

## Divisor explained

A standard incremental encoder produces 4 IRQ transitions per physical detent (click). With `divisor=4` (default), `value()` increments by 1 per detent. Set `divisor=1` to get raw transition counts, or `divisor=2` for half-step resolution.

## License

MIT License — see [LICENSE](LICENSE).
