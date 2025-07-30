"""
{{ project_name }} Application routing module.
Version: {{ version }}
"""


# Import your pages here
from .pages.counter import CounterPage

# Define {{ project_name }} routes here
routes = {
    '/': CounterPage
}