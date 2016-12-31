def get_tags(Buffer):
    tag = Buffer.create_tag
    T = [
    (["uint ", "int ", "string ", "bool ",
         "mapping", "struct ", "bytes",
         "bytes32", "address"],"#0099FF"),
    (["pragma ", "function ", "contract ", "return ", "constant "],"#0000FF"),
    (["block.", "this."], "#48C066")
    ]
    return T

def format(code):
    data = code.split("\n")
    ident = 0
    tab = "    "
    result = []
    if len(data) > 1:
        for line in data:
            if line.strip() == "}" and ident > 0:
                result.append(tab*(ident-1) + line.strip())
            else:
                result.append(tab*ident + line.strip())
            if line:
                if line[-1] == "{":
                    ident += 1
                if line.strip()[0] == "}":
                    ident -= 1
    return '\n'.join(result)

if __name__ == "__main__":
    with open("/root/contracts/test.sol", "r") as fl:
        print (format(fl.read()))
