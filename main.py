"""
uWSGI mountpoint:
The uwsgi.ini points to this module, expecting to find the callable, `app`.
"""

from registry_service import Application


app = Application('registry')
"""The uWSGI mountpoint."""
