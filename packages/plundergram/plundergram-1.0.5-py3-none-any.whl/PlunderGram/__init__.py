# PlunderGram/__init__.py

# Package metadata
__version__ = "1.0.4"
__author__ = "kpwnther"

# Importing classes and functions
from .Modules.configread import load
from .Modules.Spyglass import spyglass
from .Modules.Recon import recon 
from .Modules.Raid import raid
from .Modules.Boarding import boarding
from .Modules.JollyRoger import Flag

# Optional initialization code
print("PlunderGram has been initialized.")
