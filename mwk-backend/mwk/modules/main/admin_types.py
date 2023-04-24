from typing import Any, Collection, Protocol
from django.db.models import Model


class AdminModelForm(Protocol):
    """Protocol interface for the ModelForm used in Django admin"""

    instance: Model
    cleaned_data: dict[str, Any]
    is_bound: bool
    data: Collection
    files: Collection
    fields: dict[str, Any]
