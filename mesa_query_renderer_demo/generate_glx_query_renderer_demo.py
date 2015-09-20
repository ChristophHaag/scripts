#!/usr/bin/env python3
import csv
with open("query_renderer_test.c", "w") as cf:
    cf.write("//Compile with:\n//gcc query_renderer_demo.c -lX11 -lepoxy\n\n")
    cf.write("#include <epoxy/gl.h>\n#include <epoxy/glx.h>\n#include <stdio.h>\nint main() {\n    unsigned int value[3]; // longest return value are 3 uints\n")
    with open("query_renderer.csv") as f:
        r = csv.DictReader(f, delimiter="|")
        for row in r:
            cf.write("    " + "glXQueryRendererIntegerMESA(XOpenDisplay(NULL), 0, 0, " + row["attrib"] + ", value);\n")
            cf.write("    " + "printf(\"" + row["desc"].replace("\"","\\\"") + ":  \");\n")
            rowgen = range(int(row["returnnum"]))
            cf.write("    " + "printf(\"" + ".".join(["%u" for _ in rowgen]) + "\\n\", "
                            +  ", ".join(["value["+str(i)+"]" for i in rowgen]) + ");\n\n")
    cf.write("    return 0;\n}\n")
