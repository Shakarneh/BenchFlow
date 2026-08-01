"""Ports: what the domain NEEDS from the outside world.

This file declares interfaces only -- no database, no Django, no idea where
the data actually lives. infrastructure/repositories.py provides the real
implementation, and tests can provide a fake list instead.

That inversion is the whole point: the arrow runs infrastructure -> domain,
never domain -> infrastructure.
"""

from abc import ABC, abstractmethod


class SpecialistRepository(ABC):
    """Something that can give us Specialists. We do not care what."""

    @abstractmethod
    def all(self) -> list:
        """Return every specialist, as domain Specialist objects."""
