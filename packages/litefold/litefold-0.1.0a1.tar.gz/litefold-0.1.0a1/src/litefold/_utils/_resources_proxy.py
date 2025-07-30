from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `litefold.resources` module.

    This is used so that we can lazily import `litefold.resources` only when
    needed *and* so that users can just import `litefold` and reference `litefold.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("litefold.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
