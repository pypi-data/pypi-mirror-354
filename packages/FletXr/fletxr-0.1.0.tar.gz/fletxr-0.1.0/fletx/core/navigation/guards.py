"""
Système de protection des routes (Route Guards)
"""

from abc import ABC, abstractmethod
from typing import Any
from fletx.core.types import RouteInfo
from fletx.utils.exceptions import NavigationAborted

class RouteGuard(ABC):
    """Interface de base pour les guards"""
    
    @abstractmethod
    def can_activate(self, route: RouteInfo) -> bool:
        """Vérifie si la route peut être activée"""
        pass
    
    @abstractmethod
    def redirect(self, route: RouteInfo) -> str:
        """Retourne la route de redirection si can_activate=False"""
        pass

