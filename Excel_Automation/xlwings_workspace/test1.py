import xlwings
import xlwings as xl
from xlwings.constants import directions
from xlwings.rest import api
from xlwings.utils import rgb_to_int


def function01():
    # xl.books.
    # xl.books.open()
    xlwings.App(visible=False)
    # xlwings.apps.screen_updating: False
    wb = xl.Book("WB_test1.xlsx")
    # wb.app.screen_updating: False
    print(wb.sheets.active)
    print(wb)
    # wb.sheets(1).cells(1, 1).value = "this is test files."

    wb.close()


# function01()


def function02():
    # we are going to select the non empty cells in excel]
    # and put them into list..
    xlwings.App.screen_updating = False
    wb = xl.Book("WB_test1.xlsx")
    # wb.sheets(1).range("A1:A40000").color = rgb_to_int((255, 0, 0))
    for non_empty in wb.sheets(1).used_range:

        if non_empty.value is None:
            pass
        else:
            # print(non_empty.address)
            # wb.sheets(1).range("1:1").insert()
            non_empty.color = rgb_to_int((20, 20, 255))

    wb.sheets(1).range(cell1="A1", cell2="A10").color = rgb_to_int((255, 0, 0))

    # wb.close()
    xlwings.App.screen_updating = True


# function02()


def function03():
    xl.App.screen_updating = False
    wb = xlwings.Book("WB_test1.xlsx")
    ws = wb.sheets(1)
    #  print last cell in table
    # get last row or column values using cells.end("up", right, left, down).row/column

    print(ws.cells(1, 1).end("right").column)

    # print(ws.cells(1, 1).end(directions.xlright).column)
    # Last_col = ws.range(cell1=A1,cell2= ws.cells(1,1).end(direction=))

    for i in range(1, 1000, 2):
        ws.range(cell1=ws.cells(i,1), cell2=ws.cells(i, ws.cells(i,1).end("right").column)).insert(shift="down")
        # print(i)

    xl.App.screen_updating = True


function03()


def function04():
    pass
