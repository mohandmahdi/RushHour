def mkEnum(**enums):
    return type('Enum', (), enums)

Orientation = mkEnum(HORIZONTAL=0, VERTICAL=1)