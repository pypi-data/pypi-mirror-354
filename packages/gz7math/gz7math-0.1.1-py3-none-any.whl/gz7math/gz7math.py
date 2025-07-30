"""
GZ7Math – Experimental math library implementing the GZ7 circular model.

Key definitions
---------------
* FULL_TURN_GZ7 = 7.0   (analogous to 2π in GZ7) → corresponds to 210°
* PI_GZ7        = 3.5   (analogous to π)         → corresponds to 105°

A single GZ7‑radian therefore maps to 30° in the classical system:
    1 rad₇ = 30° = π/6 standard radians.

Conversions
-----------
    rad₇ → rad  :   x · (π/6)
    rad  → rad₇ :   r · (6/π)
    rad₇ → deg  :   x · 30
    deg  → rad₇ :   d / 30

Core trigonometric wrappers (sin7, cos7, tan7) simply convert to standard
radians and delegate to Python’s math module.  A tiny Angle class is provided
for convenience.

NOTE  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
This is an early prototype meant for experimentation.  Nothing is frozen yet:
API names, constants, and numerical conventions may evolve as the theory
matures.  Feel free to hack, break, and improve.
"""

from __future__ import annotations
import math

# ────────────────────────────────────────────────────────────────────────────
# Fundamental constants for GZ7
# ────────────────────────────────────────────────────────────────────────────
PI_GZ7: float            = 3.5
FULL_TURN_GZ7: float     = 7.0          # 2·π₇
DEG_PER_GZ7_RAD: float    = 30.0         # degrees in one GZ7‑radian
STD_RAD_PER_GZ7_RAD: float = math.pi / 6  # 30° in standard radians

# ────────────────────────────────────────────────────────────────────────────
# Unit‑conversion helpers
# ────────────────────────────────────────────────────────────────────────────

def gz7_to_rad(x: float) -> float:
    """Convert **GZ7‑radians** to **standard radians**."""
    return x * STD_RAD_PER_GZ7_RAD

def rad_to_gz7(r: float) -> float:
    """Convert **standard radians** to **GZ7‑radians**."""
    return r * 6 / math.pi

def deg_to_gz7(d: float) -> float:
    """Degrees → GZ7‑radians."""
    return d / DEG_PER_GZ7_RAD

def gz7_to_deg(x: float) -> float:
    """GZ7‑radians → Degrees."""
    return x * DEG_PER_GZ7_RAD

# ────────────────────────────────────────────────────────────────────────────
# Primary trigonometric wrappers
# ────────────────────────────────────────────────────────────────────────────

def sin7(x: float) -> float:
    """Sine of *x* where *x* is given in **GZ7‑radians**."""
    return math.sin(gz7_to_rad(x))

def cos7(x: float) -> float:
    """Cosine of *x* where *x* is given in **GZ7‑radians**."""
    return math.cos(gz7_to_rad(x))

def tan7(x: float) -> float:
    """Tangent of *x* where *x* is given in **GZ7‑radians**."""
    return math.tan(gz7_to_rad(x))

# ────────────────────────────────────────────────────────────────────────────
# Angle helper‑class (syntactic sugar)
# ────────────────────────────────────────────────────────────────────────────

class GZ7Angle:
    """Immutable angle in **GZ7‑radians** with basic arithmetic & conversion."""

    __slots__ = ("_v",)

    def __init__(self, value: float):
        self._v = float(value) % FULL_TURN_GZ7

    # ––––––––––––––––––––––––––––––––––––––––
    # Conversions & representations
    # ––––––––––––––––––––––––––––––––––––––––

    @property
    def value(self) -> float:
        """Raw value in GZ7‑radians within [0, 7)."""
        return self._v

    def to_degrees(self) -> float:
        return gz7_to_deg(self._v)

    def to_radians(self) -> float:
        return gz7_to_rad(self._v)

    # ––––––––––––––––––––––––––––––––––––––––
    # Numeric dunder methods
    # ––––––––––––––––––––––––––––––––––––––––

    def __float__(self):
        return self._v

    def __add__(self, other: float | "GZ7Angle") -> "GZ7Angle":
        return GZ7Angle(self._v + float(other))

    def __sub__(self, other: float | "GZ7Angle") -> "GZ7Angle":
        return GZ7Angle(self._v - float(other))

    def __neg__(self):
        return GZ7Angle(-self._v)

    def __repr__(self):
        return f"GZ7Angle({self._v:.6f})"

# ────────────────────────────────────────────────────────────────────────────
# Quick self‑test when run as a script
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    a = GZ7Angle(1)           # 1 rad₇ → 30°
    b = GZ7Angle(PI_GZ7)      # π₇    → 105°

    print("a in degrees:", a.to_degrees())
    print("sin7(a):", sin7(a.value))
    print("cos7(a):", cos7(a.value))
    print("b in standard radians:", b.to_radians())
"
