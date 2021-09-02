from .http import ncRequest as ncRequest
from .http import ncResponse as ncResponse

from .urls import urlPattern as ncUrlPattern
from .urls import urlPatterns as ncUrlPatterns


__all__ = (
    'ncRequest', 
    'ncResponse', 
    'ncUrlPattern', 
    'ncUrlPatterns'
)