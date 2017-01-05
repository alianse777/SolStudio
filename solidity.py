#    SolStudio
#    Copyright (C) 2017  alainse777

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
            if line.strip():
                if line.strip() == "}" and ident > 0:
                    result.append(tab*(ident-1) + line.strip())
                else:
                    result.append(tab*ident + line.strip())
                if line[-1] == "{":
                    ident += 1
                if line.strip()[0] == "}":
                    ident -= 1
            else:
                result.append(tab*ident)
    return '\n'.join(result)

if __name__ == "__main__":
    with open("/root/contracts/test.sol", "r") as fl:
        print (format(fl.read()))
