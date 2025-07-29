from update_notipy import update_notify
from importlib import metadata


__version__ = metadata.version('mrtutils')

def updateCheck():
    update_notify('mrtutils', __version__).notify()

#    ┌───────────────────────────────────────────┐
#    │                                           │
#    │   Update available 0.1.0 → 0.1.2          │
#    │   Run pip install -U pkg-info to update   │
#    │                                           │
#    └───────────────────────────────────────────┘
