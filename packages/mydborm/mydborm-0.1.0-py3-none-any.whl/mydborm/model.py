from .db import Database

class Model:
    @classmethod
    def create_table(cls):
        fields = []
        for name, field in cls.__dict__.items():
            if isinstance(field, Field):
                col = f"{name} {field.type}"
                if field.primary_key:
                    col += " PRIMARY KEY"
                if field.foreign_key:
                    col += f" REFERENCES {field.foreign_key}(id)"
                fields.append(col)
        query = f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} ({', '.join(fields)})"
        Database.execute(query)

    def save(self):
        fields = [k for k in self.__class__.__dict__ if isinstance(getattr(self, k, None), (int, str, float))]
        values = [getattr(self, f) for f in fields]
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {self.__class__.__name__.lower()} ({', '.join(fields)}) VALUES ({placeholders})"
        Database.execute(query, values)

    @classmethod
    def all(cls):
        rows = Database.execute(f"SELECT * FROM {cls.__name__.lower()}").fetchall()
        return rows
