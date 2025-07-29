"""
Config for EDeA Pydantic dataclasses.
"""

from pydantic import ConfigDict

pydantic_config = ConfigDict(extra="forbid", validate_default=False)
