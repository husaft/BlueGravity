from construct import Int8sl, Int16ub, Struct


def create_yohealth():
    yohealth_format = Struct(
        "const1" / Int16ub,
        "weight" / Int16ub,
        "unknown1" / Int16ub,
        "type" / Int8sl,
        "const2" / Int8sl,
        "const3" / Int16ub,
        "unknown2" / Int8sl,
        "const4" / Int8sl,
    )
    return yohealth_format
