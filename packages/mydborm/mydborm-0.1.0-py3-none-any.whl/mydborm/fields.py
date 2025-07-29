class Field:
    def __init__(self, field_type, primary_key=False, foreign_key=None):
        self.type = field_type
        self.primary_key = primary_key
        self.foreign_key = foreign_key

class IntField(Field):
    def __init__(self, **kwargs):
        super().__init__('INT', **kwargs)

class CharField(Field):
    def __init__(self, max_length=255, **kwargs):
        super().__init__(f'VARCHAR({max_length})', **kwargs)

class FloatField(Field):
    def __init__(self, **kwargs):
        super().__init__('FLOAT', **kwargs)

class ForeignKeyField(Field):
    def __init__(self, ref_table):
        super().__init__('INT', foreign_key=ref_table)
