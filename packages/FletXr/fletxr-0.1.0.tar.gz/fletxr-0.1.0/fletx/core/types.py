"""
FletX Types module
"""

from typing import (
    Dict, Any, Type, Optional, Callable, List, Union
)
from dataclasses import dataclass
from enum import Enum


####
##      ROUTE INFO CLASS
#####
@dataclass
class RouteInfo:
    """
    Route information
    Contains detailed information about a specific route,
    such as its path, parameters etc...
    """
    
    def __init__(
        self, 
        path: str, 
        params: Dict[str, Any] = None, 
        query: Dict[str, Any] = None
    ):
        self.path = path
        self.params = params or {}
        self.query = query or {}
        self._extra = {}

    def add_extra(self, key: str, value: Any):
        """
        Adds additional data to the route
        Allows associating additional data with a route, 
        such as metadata, security information, or context data.
        """
        self._extra[key] = value
    
    def get_extra(self, key: str, default: Any = None) -> Any:
        """
        Gets additional data
        Retrieves the additional data associated with a route, 
        such as metadata, security information, or context data.
        """
        return self._extra.get(key, default)
    

####
##      BINDING TYPE CLASS
#####
class BindingType(Enum):
    """Types of reactive bindings"""

    ONE_WAY = "one_way"          # Reactive -> Widget
    TWO_WAY = "two_way"          # Reactive <-> Widget  
    ONE_TIME = "one_time"        # Reactive -> Widget (once)
    COMPUTED = "computed"        # Computed from multiple reactives


####
##      BINDING CONFIGURATION CLASS
#####
@dataclass
class BindingConfig:
    """Configuration for a reactive binding"""

    reactive_attr: str
    binding_type: BindingType = BindingType.ONE_WAY
    transform_to_widget: Optional[Callable[[Any], Any]] = None
    transform_from_widget: Optional[Callable[[Any], Any]] = None
    validation: Optional[Callable[[Any], bool]] = None
    on_change: Optional[Callable[[Any, Any], None]] = None  # (old_value, new_value)
    condition: Optional[Callable[[], bool]] = None
    debounce_ms: Optional[int] = None
    throttle_ms: Optional[int] = None


####
##      COMPUTED BINDING CONFIGURATION CLASS
#####
@dataclass
class ComputedBindingConfig:
    """Configuration for computed reactive bindings"""

    compute_fn: Callable[[], Any]
    dependencies: List[str]  # Names of reactive attributes
    transform: Optional[Callable[[Any], Any]] = None
    on_change: Optional[Callable[[Any, Any], None]] = None


####
##      REATIVE FORM VALIDATION RULE CLASS
#####
@dataclass
class FormFieldValidationRule:
    """Form Field Validation rule"""

    validate_fn: Union[str, Callable[[Union[str,int,float,bool]],bool]] 
    err_message: str
