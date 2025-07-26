"""Data models for Linq-AcmeCRM integration."""

from .linq_models import LinqContact, LinqContactResponse
from .acme_models import AcmeContact, AcmeContactResponse

__all__ = ["LinqContact", "LinqContactResponse", "AcmeContact", "AcmeContactResponse"]
