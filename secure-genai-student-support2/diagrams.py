"""Diagram asset paths — works whether files are flat or in a subfolder."""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
AI_ARCH_SVG = os.path.join(_HERE, "assets_ai.png")
NETWORK_SVG  = os.path.join(_HERE, "assets_net.png")
