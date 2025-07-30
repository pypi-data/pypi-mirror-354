"""
Middleware pour intercepter la navigation
"""

from typing import Callable, Any, Optional
from fletx.core.types import RouteInfo

class NavigationMiddleware:
    """Middleware de navigation"""
    
    def __init__(self):
        self._before_handlers = []
        self._after_handlers = []
    
    def add_before_handler(self, handler: Callable[[RouteInfo], Optional[str]]):
        """Ajoute un handler avant navigation"""
        self._before_handlers.append(handler)
    
    def add_after_handler(self, handler: Callable[[RouteInfo], None]):
        """Ajoute un handler après navigation"""
        self._after_handlers.append(handler)
    
    def run_before(self, route: RouteInfo) -> Optional[str]:
        """Exécute les handlers avant navigation"""
        for handler in self._before_handlers:
            result = handler(route)
            if result is not None:
                return result
        return None
    
    def run_after(self, route: RouteInfo):
        """Exécute les handlers après navigation"""
        for handler in self._after_handlers:
            handler(route)