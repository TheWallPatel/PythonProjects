# import os

import xlwings as xl

def function01():
    try:
        # xlapp = xl.apps.add()
        # xlapp.
        # wb = xl.Book()

        Excel01 = xl.Book("./Excel01.xlsx")
        Excel02 = xl.Book("./Excel02.xlsx")

        Excel01.activate()
        # wb.name = "this"

        sh = Excel01.sheets.active
        # sh.range("A1").value = "dhawal"
        sh.range("A1").color = "#0000FF"
        # wb.sheets[0].range("A1") = "dhawal"

        print(sh)

    except OSError as err:
        print(f"OSerror: {err}")
        # pass
    else:
        pass
        # print(type(var1))



function01()

def function02():
    bob = xl.Book()
    # bob.fullname
    # bob.fullname = "dhawa"
    # bob.fullname = "dhawal"
    print(bob.name)


# function02()