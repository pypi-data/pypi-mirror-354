# PlunderGram/__init__.py

# Package metadata
__version__ = "1.0.0"
__author__ = "kpwnther"

# Importing classes and functions
from .configread import load
from .Spyglass import spyglass
from .Recon import recon 
from .Raid import raid
from .Boarding import boarding
from .JollyRoger import Flag

# Optional initialization code
print("PlunderGram has been initialized.")
