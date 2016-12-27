def get_tags(Buffer):
    tag = Buffer.create_tag
    T = [
    (["uint", "int", "string", "bool",
         "mapping", "struct", "bytes",
         "bytes32", "address"],"#0099FF"),
    (["pragma", "function", "contract", "return"],"#0000FF"),
    (["block", "this"], "#48C066")
    ]
    return T