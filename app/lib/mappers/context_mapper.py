from bson import ObjectId

def context_to_json_mapper(document):
    """Convert MongoDB document to a serializable dictionary."""
    if isinstance(document, dict):
        return {k: context_to_json_mapper(v) for k, v in document.items()}
    elif isinstance(document, ObjectId):
        return str(document)
    return document