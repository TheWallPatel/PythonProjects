import sys
import os
from os.path import exists
import xlwings as xl
from xlwings import constants

import re
xl.App.display_alerts = False
xl.App.screen_updating = True
xl.App.visible = True


class Init_Workbook:

    wb_in = ""
    in_sh = ""
    wb_template = ""
    templ_sh = ""
    wb_out = ""
    out_sh = ""

    subform_found = False


    # inpur cust/Exte WB. format of Cust and Exter are same no col change
    Cust_Dept_col = 1
    Cust_SubF_col = 2
    Cust_Month_List = {"Jan-21":3, "Feb-21":29, "Mar-21":55, "Apr-21":81, "May-21":107, "Jun-21":133,
                  "Jul-21":159, "Aug-21":185, "Sept-21":211, "Oct-21":237, "Nov-21":263, "Dec-21":289}

    get_Cust_offset_col = {"LE0": 17,"LE1": 2,"LE2": 5,"LE3": 8,"LE4": 11,"LE5": 14 }



    # data_source_file_columns
    DS_col = ["Country","DEPT","BRAND","CATEGORY","RANGE","FORM","SUB FORM",
                            "$$$ (1,000 LC)","MONTH","ACT/EST","*CP/ES*","SUBMISSION DATE"]



    # loop list
    Purchase_list = ["CUSTOMER PURCHASE","EXTERNAL SALES"]
    # Submission_date = ["Jan-21","Feb-21","Mar-21","Apr-21","May-21","Jun-21",
    #                    "Jul-21","Aug-21","Sept-21","Oct-21","Nov-21","Dec-21"]
    Submission_date = []
    Month_List = ["Jan-21","Feb-21","Mar-21","Apr-21","May-21","Jun-21",
                       "Jul-21","Aug-21","Sept-21","Oct-21","Nov-21","Dec-21"]
    # Data_temp copy pasting
    dept_temp_start_row = 2
    dept_temp_end_row = 0
    dept_temp_start_col = 1
    dept_temp_end_col = 0

    PC_Subforms = {"INTEGRATE": 2.1,"Za":2.1,"MJ":2.1,"MQ":2.1,
                   "RE":2.1,"HAKU":2.1,"Ettusais":2.1,
                   "OTHERS (1)":2.1,"UNO (FI & SK)":2.1,"TISS (FI & SK)":2.1,
                   "OTHERS (2)":2.1}
    Brands_dict = {"ME":7,"CP":7,"NA":7,"LAME":7,"IP":7,"DREL":7,"BARE":7,"BQ":7,"DICI":7,"ME":7,
                   "D & G":3,"D & G MAKEUP":3,"OTHER DESIGNERS":3,"SEN":6,"D-PROGRAM":6,"ANES":6,
                   "TSU":6,"ELIX":6,"COSMETIC OTHERS":4,"PC OTHERS":4}


    def __init__(self,In_wb,template,out_wb):
        try:

            if( os.path.exists(In_wb) == False):
                print(f"Input_file :{In_wb +'.xlsx'} does not exit")
            if(os.path.exists(template) == False):
                print(f"Input_file :{template} does not exit")
            if (os.path.exists("./" + out_wb + ".xlsx") == False):
                print(f"Input_file :{out_wb + '.xlsx'} does not exit")
        except OSError as err2:
            print(f"error : {err2}")
        else:
            try:
                Init_Workbook.wb_in = xl.Book(In_wb)
                Init_Workbook.wb_in.app.visible = False
                # Init_Workbook.wb_in
                # in_sh will decided by purchase list.
                Init_Workbook.wb_template = xl.Book(template)
                Init_Workbook.wb_template.app.visible = False
                Init_Workbook.templ_sh = Init_Workbook.wb_template.sheets("Dept_Template")
                # init Data_template file
                Init_Workbook.dept_temp_end_row = Init_Workbook.templ_sh.cells(1, 2).end("down").row
                Init_Workbook.dept_temp_end_col = Init_Workbook.templ_sh.cells(1, 1).end("right").column

                # this create new workbooks and add sheet with name "Data Source"
                Init_Workbook.wb_out = xl.Book()
                Init_Workbook.wb_out.sheets.add("Data Source")
                Init_Workbook.out_sh = Init_Workbook.wb_out.sheets("Data Source")

                print(Init_Workbook.templ_sh.cells(1,1).end("right").column)
                for i in range(1,(Init_Workbook.templ_sh.cells(1,1).end("right").column)+1):
                    Init_Workbook.out_sh.cells(1,i).value = Init_Workbook.templ_sh.cells(1,i).value

                Init_Workbook.wb_out.save("./"+ out_wb +".xlsx")
                Init_Workbook.wb_out.app.visible = False
                # Init_Workbook.wb_out.activate()

                print("opened Succesfully")

            except OSError as err:
                print(f"Error: {err}")
                self.__del__()
            else:
                pass

    def __del__(self):
        Init_Workbook.wb_template.save()
        Init_Workbook.wb_in.save()
        Init_Workbook.wb_out.save()
        Init_Workbook.wb_template.close()
        Init_Workbook.wb_in.close()
        Init_Workbook.wb_out.close()
        print("closed all files successufully")


    def mapping01(self,mapp_sh,submit_date):
        start_row = 2
        start_col = 1
        end_row = mapp_sh.cells(1,1).end("down").row
        temp_mapp = ""
        for ran1 in mapp_sh.range("A1:A20"):
            if (ran1.value != None and ran1.value== submit_date ):
                temp_mapp = mapp_sh.cells(ran1.row,2).value
                break

        return temp_mapp

    def find_Subf_val(self,Data_sh,Sh_name,month1,brand,sub_form,dept_value):
        # this fuction finds the columns in Customer 1_2 and 2_2 sheet
        # Sheet_name = ""
        brand_Start_row = 0
        brand_end_row = 0
        sub_form_Col = 2
        temp02_subform = ""
        temp_data = 0

        if (brand == "PC"):
            var01 = 10

        Data_sh11 = Data_sh.sheets(Sh_name)

        #its only for FRG
        if (dept_value =="FRG"):

            for ran2 in Data_sh11.range(f"A1:A200"):
                temp_ran2 = str(ran2.value).strip(" \n")
                if (temp_ran2 == dept_value):
                    brand_Start_row = ran2.row
                    break

            if (brand_Start_row != 0):
                for ran3 in Data_sh11.range(f"B{brand_Start_row}:B200"):
                    temp_ran3 = str(ran3.value).strip(" \n")
                    if (temp_ran3 == f"{dept_value} TOTAL"):
                        brand_end_row = ran3.row
                        break
            else:
                print(f"Dept {dept_value}  is not found  in {Sh_name}")

        # this is for PC only
        elif (dept_value == "PC" and Sh_name == "2_1" ):

            for ran2 in Data_sh11.range(f"A1:A200"):
                temp_ran2 = str(ran2.value).strip(" \n")
                if (temp_ran2 == dept_value):
                    brand_Start_row = ran2.row
                    break

            if (brand_Start_row != 0):
                for ran3 in Data_sh11.range(f"B{brand_Start_row}:B200"):
                    temp_ran3 = str(ran3.value).strip(" \n")
                    if (temp_ran3 == f"{dept_value} TOTAL"):
                        brand_end_row = ran3.row
                        break
            else:
                print(f"Dept {dept_value}  is not found  in {Sh_name}")
        else:
            for ran1 in Data_sh11.range("A1:A200"):
                temp_ran1 = str(ran1.value).strip(" \n")
                # print(temp_ran1)
                if (temp_ran1 == brand):
                    brand_Start_row = ran1.row
                elif(brand_Start_row != 0 and ran1.value == (brand +" TOTAL (1)")):
                    brand_end_row = ran1.row
                    break
                elif (brand_Start_row != 0 and ran1.value == (brand + " TOTAL")):
                    brand_end_row = ran1.row
                    break

        if(brand_Start_row != 0):
            for i in range(brand_Start_row,brand_end_row+1):
                # if(Data_sh11)
                temp02_subform = str(Data_sh11.cells(i,sub_form_Col).value).strip(" \n")
                if (temp02_subform == sub_form):
                    self.subform_found = True
                    temp_data = Data_sh11.cells(i,month1).value
                    break
            if(temp02_subform == "None"):
                temp_data = 0
                print(f"Value not found: Dept:{dept_value}-->brand{brand}-->Sub-Form:{sub_form} in Sheet:{Sh_name} ")
        else:
            # if (brand =="DREL"):
            temp_data=0
            print(f"Brand {brand} Not Found in Sheet {Sh_name}")

        return temp_data


    def find_ACT_EST(self,IN_WB,month1,pur_list):
        sheet_name = ""
        month_col = self.Cust_Month_List.get(month1)
        if pur_list =="CUSTOMER PURCHASE":
            sheet_name = "1_2"
        else:
            sheet_name = "2_2"
            #returning first column of every month in 1_2 & 2_2
        return IN_WB.sheets(sheet_name).cells(14,month_col).value

    def find_ACT_EST_11(self,IN_WB,month1,pur_list):
        sheet_name = ""
        month_col = self.Cust_Month_List.get(month1)
        if pur_list =="CUSTOMER PURCHASE":
            sheet_name = "1_2"
        else:
            sheet_name = "2_2"
            #returning first column of every month in 1_2 & 2_2
        return IN_WB.sheets(sheet_name).cells(14,month_col).value







    # before calling this function, make sure Data_source_init in called
    def Fill_Data(self,in_wb,templ_sh,out_sh):
        Dept_value= ""
        purchase_list = ""
        sheet_name = ""
        Sh_2_3_Offset = 0
        value_to_fetch = ""
        cur_row = 0

        for mon in Init_Workbook.Month_List:

            cur_mon = self.Cust_Month_List.get(mon)
            if(out_sh.cells(2,2).value ==None):
                cur_row=2
            else:
                cur_row = out_sh.cells(1,2).end("down").row + 1

            # copy each dept_temp into DATA Source sheet row by row

            for i in range(2, self.dept_temp_end_row+1):
                cur_ds_col = self.DS_col.index("Country") + 1
                if (i == 264):
                    if (1 == 1):
                        pass

                # from col 1 to 6
                for col in range(1, self.dept_temp_end_col+1):

                    out_sh.cells(cur_row,cur_ds_col).value = templ_sh.cells(i,col).value
                    cur_ds_col = cur_ds_col + 1

                # fill the other cols like month, submission_data, LE
                out_sh.cells(cur_row, 9).value = mon
                out_sh.cells(cur_row, 11).value = templ_sh.cells(i,11).value
                # out_sh.cells(cur_row, 12).value = Submit_date

                Dept_value = out_sh.cells(cur_row, 2).value
                purchase_list = out_sh.cells(cur_row, 11).value

                #for testing only
                if (Dept_value == "FRG"):
                    if (1==1):
                        pass



                #get the submission date
                if (Dept_value == "PRES" and purchase_list =="CUSTOMER PURCHASE"):
                    sheet_name = "1_2"
                    out_sh.cells(cur_row, 12).value = in_wb.sheets(sheet_name).cells(9, 2).value
                elif (Dept_value == "PRES" and purchase_list =="EXTERNAL SALES"):
                    sheet_name = "2_2"
                    out_sh.cells(cur_row, 12).value = in_wb.sheets(sheet_name).cells(9, 2).value
                elif (Dept_value == "FRG" and purchase_list =="CUSTOMER PURCHASE"):
                    sheet_name = "1_1"
                    out_sh.cells(cur_row, 12).value = in_wb.sheets(sheet_name).cells(9, 2).value
                elif (Dept_value == "FRG" and purchase_list =="EXTERNAL SALES"):
                    sheet_name = "2_1"
                    out_sh.cells(cur_row, 12).value = in_wb.sheets(sheet_name).cells(9, 2).value

                elif(Dept_value == "PC" and (out_sh.cells(cur_row,3).value == "COSMETIC OTHERS" or out_sh.cells(cur_row,3).value == "PC OTHERS") ):
                    sheet_name = "2_1"
                    out_sh.cells(cur_row, 12).value = in_wb.sheets(sheet_name).cells(9, 2).value
                elif (Dept_value == "PC"):
                    # if (self.PC_Subforms.get((out_sh.cells(cur_row, 7).value),False) == 0 ):
                    sheet_name = "2_3"
                    out_sh.cells(cur_row, 12).value = in_wb.sheets(sheet_name).cells(9, 2).value



                if (sheet_name == "2_3"):
                    value_to_fetch = out_sh.cells(cur_row,self.Brands_dict.get(str(out_sh.cells(cur_row,3).value))).value
                    Sh_2_3_Offset = 1
                    # fetching ACT/EST string values
                    out_sh.cells(cur_row, 10).value = in_wb.sheets(sheet_name).cells(14, cur_mon + Sh_2_3_Offset).value
                    temp_d1 = self.find_Subf_val(in_wb,sheet_name,(cur_mon +Sh_2_3_Offset),out_sh.cells(cur_row,3).value,value_to_fetch,Dept_value)
                    # if not found in 2_3 then find in 2_1
                    # if(self.subform_found == False):
                    #     temp_d1 = self.find_Subf_val(in_wb,"2_1", (cur_mon),
                    #                                  out_sh.cells(cur_row, 3).value, out_sh.cells(cur_row, 7).value)
                    #     #once found put External sales
                    #     if(temp_d1 !=0):
                    #         out_sh.cells(cur_row, 12).value = in_wb.sheets("2_1").cells(9, 2).value

                else:
                    value_to_fetch = out_sh.cells(cur_row,
                                                  self.Brands_dict.get(str(out_sh.cells(cur_row, 3).value))).value
                    Sh_2_3_Offset = 0
                    # fetching ACT/EST string values
                    out_sh.cells(cur_row, 10).value = in_wb.sheets(sheet_name).cells(14, cur_mon + Sh_2_3_Offset).value
                    temp_d1 = self.find_Subf_val(in_wb,sheet_name,(cur_mon +Sh_2_3_Offset),out_sh.cells(cur_row,3).value,value_to_fetch,Dept_value)

                if temp_d1 != 0 : out_sh.cells(cur_row, 8).value = temp_d1


                cur_row += 1
                Sh_2_3_Offset = 0
                self.subform_found = False
            # self.wb_out.save()



try:
    temp = Init_Workbook(sys.argv[1],sys.argv[2],sys.argv[3])
    # temp = Init_Workbook("./Input_file_test.xlsx","./Dept_Template_test.xlsx","output_file04")
    y = temp.Fill_Data(temp.wb_in,temp.templ_sh,temp.out_sh)
    temp.__del__()
except OSError as err1:
    temp.__del__()
    print(f"Error Occured: {err1}")
except KeyboardInterrupt as keyerr:

    temp.__del__()
    print(f"Keyboard Interrupt Error Occured: {keyerr}")
except BaseException as base11:
    print(f"Base Exception: {base11} type= {type(base11)}")
    temp.__del__()
else:
    pass


