"""
Decorators for route registration.

These decorators simplify the process of associating URL routes with 
their corresponding page handlers, enabling clear and concise routing 
definitions within the application.
"""

from typing import Type, Callable
from fletx.core.route_config import RouteConfig
from fletx.core.page import FletXPage


####    REGISTER ROUTE
def register_route(path: str):
    """Decorator to automatically register a route"""

    def decorator(page_class: Type[FletXPage]):
        RouteConfig.register_route(path, page_class)
        return page_class
    return decorator