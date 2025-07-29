from typing import TypeIs, TypeGuard, Any
from .aliases import (
    JsonNumber,
    JsonScalar,
    JsonArray,
    JsonObject,
    JsonDocument,
    Json,
    JsonArrayOf,
    JsonObjectOf,
    JsonDocumentOf,
)

# Is (not deep)

def is_json_number(obj: Any) -> TypeIs[JsonNumber]:
    """Narrowed with `TypeIs`. Note: Also ensures it's NOT `bool`"""

def is_json_scalar(obj: Any) -> TypeIs[JsonScalar]:
    """Narrowed with `TypeIs`"""

def is_json_array(obj: Any) -> TypeIs[JsonArrayOf[Any]]:
    """Narrowed with `TypeIs`. NOT deep-checked. Use `..._deep` if needed."""

def is_json_object(obj: Any) -> TypeIs[JsonObjectOf[Any, Any]]:
    """Narrowed with `TypeIs`. NOT deep-checked. Use `..._deep` if needed."""

def is_json_document(obj: Any) -> TypeIs[JsonDocumentOf[Any, Any, Any]]:
    """Narrowed with `TypeIs`. NOT deep-checked. Use `..._deep` if needed."""

def is_json(obj: Any) -> TypeIs[JsonScalar | JsonDocumentOf[Any, Any, Any]]:
    """Narrowed with `TypeIs`. NOT deep-checked. Use `..._deep` if needed."""

# Guard (not deep)

def guard_json_number(obj: Any) -> TypeGuard[JsonNumber]:
    """Narrowed with `TypeGuard`. Note: Also ensures it's NOT `bool`"""

def guard_json_scalar(obj: Any) -> TypeGuard[JsonScalar]:
    """Narrowed with `TypeGuard`"""

def guard_json_array(obj: Any) -> TypeGuard[JsonArrayOf[Any]]:
    """Narrowed with `TypeGuard`. NOT deep-checked. Use `..._deep` if needed."""

def guard_json_object(obj: Any) -> TypeGuard[JsonObjectOf[Any, Any]]:
    """Narrowed with `TypeGuard`. NOT deep-checked. Use `..._deep` if needed."""

def guard_json_document(obj: Any) -> TypeGuard[JsonDocumentOf[Any, Any, Any]]:
    """Narrowed with `TypeGuard`. NOT deep-checked. Use `..._deep` if needed."""

def guard_json(obj: Any) -> TypeGuard[JsonScalar | JsonDocumentOf[Any, Any, Any]]:
    """Narrowed with `TypeGuard`. NOT deep-checked. Use `..._deep` if needed."""

# Is (deep)

def is_json_array_deep(obj: Any) -> TypeIs[JsonArray]:
    """Narrowed with `TypeIs`. Deep-checked recursively."""

def is_json_object_deep(obj: Any) -> TypeIs[JsonObject]:
    """Narrowed with `TypeIs`. Deep-checked recursively."""

def is_json_document_deep(obj: Any) -> TypeIs[JsonDocument]:
    """Narrowed with `TypeIs`. Deep-checked recursively."""

def is_json_deep(obj: Any) -> TypeIs[Json]:
    """Narrowed with `TypeIs`. Deep-checked recursively."""

# Guard (deep)

def guard_json_array_deep(obj: Any) -> TypeGuard[JsonArray]:
    """Narrowed with `TypeGuard`. Deep-checked recursively."""

def guard_json_object_deep(obj: Any) -> TypeGuard[JsonObject]:
    """Narrowed with `TypeGuard`. Deep-checked recursively."""

def guard_json_document_deep(obj: Any) -> TypeGuard[JsonDocument]:
    """Narrowed with `TypeGuard`. Deep-checked recursively."""

def guard_json_deep(obj: Any) -> TypeGuard[Json]:
    """Narrowed with `TypeGuard`. Deep-checked recursively."""
