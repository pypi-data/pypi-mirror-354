[project]
name = "{{ name }}"
version = "{{ version }}"
description = "{{ description }}"
readme = "README.md"
authors = [{ name = "{{ author }}", email = "" }]
requires-python = ">={{ python_version }}"
dependencies = [
    "fletx",
    "flet[all]",
]