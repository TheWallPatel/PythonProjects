import sys
import time

import xlwings as xl
import os
xl.App.screen_updating = False
xl.App.display_alerts = False
xl.App.visible = False

class Init01:
    In_wb = ""
    In_sh = []
    Out_wb = ""
    Out_sh = []

    In_file_col = {"First Name" : 3,"Last Name":4,"Prospect Position":5,"Company Name":6}
    Out_file_col = {"Company Name": 1, "First Name":3, "Last Name":4}

    Outfile_dict = {}
    input_file_path = ""

    input_folder = "./Input_files"
    output_folder = "./Output_file"


    def __init__(self):
        try:

            print("Python Script is running:")
            if (os.path.exists(self.input_folder) == False):
                print(f"InputFile folder: {self.input_folder} does not exits")
            if (os.path.exists(self.output_folder) == True):
                temp_path = 0
                temp_path = os.listdir(self.output_folder)[0]
                if temp_path != 0:
                    self.Out_wb = xl.Book(self.output_folder +"/"+ temp_path)
                    self.Out_sh = self.Out_wb.sheets(1)
                    if(self.Out_sh == None):
                        print("Required sheet is not available in Output file please check")
            else:
                print(f"OutFile folder: {self.output_folder} does not exits")
                self.__del__()
        except:
            print("error raise while check files exits or not")
        else:
            pass


    def __del__(self):
        # self.In_wb.save()
        # self.In_wb.close()
        # self.Out_wb.save()
        # self.Out_wb.close()

        print("Files are Saved and Close Successfully")


    def Inert_data(self,in_sh,out_sh,file_name):
        in_sh.activate()
        out_sh.activate()
        Line_search = 1000
        In_end_row = in_sh.cells(1,3).end("down").row

        curr_comp_found_count = 0
        in_to_out_comp_found = False

        range_str = str("C2" + ":D" + str(In_end_row))
        curr_comp_found_count = In_end_row -1
        temp_select = in_sh.range(range_str).value
        # out_sh.activate()

        out_comp_row = 2

        out_comp_row_addr = f"A{str(out_comp_row + 1)}:Z{str(out_comp_row + 1)}"
        for k in range(out_comp_row + 1, (out_comp_row + curr_comp_found_count) + 1):
            out_sh.range(out_comp_row_addr).insert("down")


        out_sh.range(f"C{out_comp_row + 1}:D{out_comp_row + curr_comp_found_count}").value = temp_select

        in_to_out_comp_found = True

        return in_to_out_comp_found

try:
    # print(f"{sys.argv[1], sys.argv[2]}")
    # temp = Init01(sys.argv[1],sys.argv[2])
    # temp = Init01("./FloatMe_test.csv","./Prospects_test.xlsx")

    temp = Init01()
    if(temp.Out_sh != None):
        for path11 in os.listdir(temp.input_folder):
            path11 = "AXLEBOLT LTD.csv"
            temp.In_wb = xl.Book(temp.input_folder +'/'+ path11)
            abc = xl.books.active
            # print(xl.books.active)
            # print(type(temp.In_wb))
            temp.In_sh = temp.In_wb.sheets(1)
            temp.In_sh.activate()
            if (temp.In_sh != None):

                x1 = temp.Inert_data(temp.In_sh,temp.Out_sh,path11[0:(len(path11)-5)+1])
                temp.In_wb.close()
                temp.In_wb = None

            else:
                print(f"File : {temp.input_folder + '/' + path11} cannot be open")
        # print(xl.books.active)
        temp.Out_wb.save()
        temp.Out_wb.close()
        temp.Out_wb = None

except OSError as err:
    print(f"Exception Occured : {err}")
    temp.__del__()
except BaseException as base11 :
    print(f"base expection {base11}")
else:
    pass