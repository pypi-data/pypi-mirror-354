"""
Gestion des transitions entre pages
"""

import enum
import flet as ft
from typing import Optional, Dict, Any, Callable
from functools import partial

class TransitionType(enum.Enum):
    NATIVE = "native"
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM = "zoom"
    CUSTOM = "custom"

class RouteTransition:
    """Configuration de transition"""
    
    def __init__(
        self,
        transition_type: TransitionType = TransitionType.NATIVE,
        duration: int = 300,
        custom_transition: Optional[Callable] = None
    ):
        self.type = transition_type
        self.duration = duration
        self.custom = custom_transition
    
    def apply(self, page: ft.Page, controls: list):
        """Applique la transition"""
        if self.type == TransitionType.FADE:
            return self._apply_fade(page, controls)
        elif self.type == TransitionType.SLIDE_LEFT:
            return self._apply_slide(page, controls, -1)
        # ... autres transitions
        
    def _apply_fade(self, page: ft.Page, controls: list):
        """Transition de fondu"""
        for control in controls:
            control.opacity = 0
            control.update()
            
        def animate():
            for control in controls:
                control.opacity = 1
                control.update()
        
        page.animate_opacity(self.duration, animate)
    
    # ... autres méthodes de transition