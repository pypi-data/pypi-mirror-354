"""
This module contains the types for the apps
depending on the builder used.
This module imports all the apps and their types
and sets them as attributes on the App class, if they are available.
If they are not available, they are set to Any, so that we can add
an import exception to the app.


"""

from typing import Any, Protocol, cast
import logging
from typing import Dict, TYPE_CHECKING
from koil import unkoil
from koil.composition import KoiledModel
from arkitekt_next.base_models import Manifest
from fakts_next import Fakts
from herre_next import Herre


if TYPE_CHECKING:
    from rekuest_next.rekuest import RekuestNext


logger = logging.getLogger(__name__)


class App(Protocol):
    """An app that is built with the easy builder"""

    fakts: Fakts
    herre: Herre
    manifest: Manifest
    services: Dict[str, KoiledModel]

    @property
    def rekuest(self) -> "RekuestNext":
        """Get the rekuest service"""
        if "rekuest" not in self.services:
            raise ValueError("Rekuest service is not available")
        return cast("RekuestNext", self.services["rekuest"])

    def run(self):
        return unkoil(self.rekuest.arun)

    async def arun(self):
        return await self.rekuest.arun()

    def run_detached(self):
        """Run the app detached"""
        return self.rekuest.run_detached()

    def register(self, *args, **kwargs):
        """Register a service"""

        self.rekuest.register(*args, **kwargs)

    async def __aenter__(self):
        await super().__aenter__()
        for service in self.services.values():
            await service.__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        for service in self.services.values():
            await service.__aexit__(exc_type, exc_value, traceback)


class Builder(Protocol):
    """A protocol for a builder class.

    This protocol defines the methods that a builder class must implement.
    """

    def __call__(self, *args: Any, **kwds: Any) -> Any: ...
