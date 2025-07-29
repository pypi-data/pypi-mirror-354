type JsonNumber = int | float
type JsonScalar = str | JsonNumber | bool | None

# Fully specialized
type JsonArray = list[Json]
type JsonObject = dict[str, Json]
type JsonDocument = JsonArray | JsonObject
type Json = JsonScalar | JsonDocument

# Takes generic arguments
type JsonArrayOf[T: Json = Json] = list[T]
type JsonObjectOf[KT: str = str, VT: Json = Json] = dict[KT, VT]
type JsonDocumentOf[T: Json = Json, KT: str = str, VT: Json = Json] = (
    JsonArrayOf[T] | JsonObjectOf[KT, VT]
)
type JsonOf[T: Json = Json, KT: str = str, VT: Json = Json] = (
    JsonScalar | JsonDocumentOf[T, KT, VT]
)
