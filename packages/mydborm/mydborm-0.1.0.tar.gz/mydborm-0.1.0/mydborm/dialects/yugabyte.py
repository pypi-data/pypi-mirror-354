def get_column_type(field):
    if field.__class__.__name__ == "IntField":
        return "INT"
    elif field.__class__.__name__ == "CharField":
        return "TEXT"  # YugaByte handles strings as TEXT
    else:
        raise TypeError("Unsupported field type for YugaByteDB")
