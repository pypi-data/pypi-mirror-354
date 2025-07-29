def get_column_type(field):
    if field.__class__.__name__ == "IntField":
        return "INT"
    elif field.__class__.__name__ == "CharField":
        return f"VARCHAR({field.max_length})"
    else:
        raise TypeError("Unsupported field type for MySQL")
