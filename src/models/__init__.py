# models/__init__.py
from .historical_site import HistoricalSite
from .historical_event import HistoricalEvent
from .user import User
from .contribution import Contribution
from .comment import Comment

# And perhaps expose them in a list to easily import all at once elsewhere
__all__ = ["HistoricalSite", "HistoricalEvent", "User", "Contribution", "Comment"]
