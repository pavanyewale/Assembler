from __future__ import print_function
def print_table(name,header,table):
    print()
    print("\t\t"+name)
    for h in header:
        print(h,end="\t")
    print()
    for entry in table:
        for d in entry:
            print(d,end="\t")
        print()
    print()
