# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["StructurePredictionSubmitParams"]


class StructurePredictionSubmitParams(TypedDict, total=False):
    job_name: Required[str]

    model_name: Required[str]

    existing_job_name: Optional[str]

    files: Optional[List[FileTypes]]
