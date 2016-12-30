def get_tags(Buffer):
    tag = Buffer.create_tag
    T = [
    (["uint", "int", "string", "bool",
         "mapping", "struct", "bytes",
         "bytes32", "address"],"#0099FF"),
    (["pragma", "function", "contract", "return", "constant"],"#0000FF"),
    (["block", "this"], "#48C066")
    ]
    return T

def format(code):
    data = code.split("\n")
    ident = 0
    tab = "    "
    result = []
    for line in data:
        result.append(tab*ident + line)
        if line:
            if line[-1] == "{":
                ident += 1
            if line.strip()[0] == "}":
                ident -= 1
    return '\n'.join(result)

if __name__ == "__main__":
    with open("/root/contracts/test.sol", "r") as fl:
        print (format(fl.read()))
