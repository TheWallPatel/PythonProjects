from selenium import webdriver
import time
import json
import pandas as pd

def function():
    data = []
    temp_str = []
    #init web driver
    driver01 = webdriver.Chrome("./chromedriver")
    #Static URL given
    driver01.get("https://www.abstractsonline.com/pp8/#!/9330/sessions/@timeslot=Sep28/1")
    #wait for page load
    time.sleep(10)

    #finding number of output appear in session results
    span9 = driver01.find_element_by_class_name("span9")
    ul_list = span9.find_element_by_id("results")
    li_list = ul_list.find_elements_by_tag_name("li")

    # running for every iten in list
    for i in range(len(li_list)):
        # time.sleep(5)
        span9 = driver01.find_element_by_class_name("span9")
        ul_list = span9.find_element_by_id("results")
        li_list = ul_list.find_elements_by_tag_name("li")
        print(f"Inside List Element displayed : { li_list[i].is_displayed()}")

        row_fuild = li_list[i].find_element_by_class_name("row-fluid")
        span9_01 = row_fuild.find_element_by_class_name("span9")
        i_element_page = span9_01.find_element_by_class_name("title").click()


        time.sleep(10)

        inner_class = driver01.find_element_by_class_name("inner")

        span10_offset1_title = inner_class.find_element_by_class_name("offset1")
        span10_offset1_row_fuild = span10_offset1_title.find_element_by_class_name("row-fluid")
        # span10_row_fuild_span9 = span10_offset1_row_fuild.find_element_by_class_name("span9")
        span9_02 = span10_offset1_row_fuild.find_element_by_id("spnSessionTitle")
        session_title = span9_02.text
        print(session_title)
        table00  = span10_offset1_title.find_element_by_class_name("table")
        session_date_class = table00.find_element_by_class_name("session-date")
        temp_str = str(session_date_class.text).split(",")
        session_date = temp_str[0] +temp_str[1]
        print(session_date)
        session_time = temp_str[2]
        session_loc_class = table00.find_element_by_class_name("session-location")
        session_loc = session_loc_class.text
        print(session_loc)
        print(driver01.current_url)

        presentation_table_class = inner_class.find_element_by_class_name("presentation-table")
        all_session_table = presentation_table_class.find_element_by_class_name("table")
        tboady_tag = all_session_table.find_element_by_tag_name("tbody")
        tr_tags = tboady_tag.find_elements_by_tag_name("tr")
        print(f"Len of table = {len(tr_tags)}")
        Author_name = ""
        Author_affil = ""
        Abstract_Number = ""
        sub_session_title = ""
        Abstract_text = ""
        if(len(tr_tags)>1):
            for i in range(1,2): # running for 2nd Sub session Only,first sub-session is ignored
                    participants_00 = tr_tags[i].find_element_by_class_name("participants")
                    Author_name_tag = participants_00.find_element_by_tag_name("b")
                    Author_name = str(Author_name_tag.text).split(",")
                    Author_affil = participants_00.text
                    title_link = tr_tags[i].find_element_by_class_name("title")
                    Abstract_Number_str = str(title_link.text).split("-")
                    Abstract_Number = Abstract_Number_str[0]
                    sub_session_title_tag = title_link.find_element_by_tag_name("b")
                    sub_session_title = sub_session_title_tag.text
                    tr_tags[i].find_element_by_class_name("title").click()

                    # move into abstract page
                    time.sleep(7) # loading page
                    Abstract_page  = driver01.find_element_by_class_name("span7")
                    dl_tag = Abstract_page.find_element_by_tag_name("dl")
                    dds_tags = dl_tag.find_elements_by_tag_name("dd")
                    Abstract_text = dds_tags[len(dds_tags)-1].text
                    time.sleep(5)
                    driver01.back()

                    #Value check:
                    # print(Author_name)
                    # print(Author_affil)
                    # print(Abstract_Number)
                    # print(sub_session_title)
                    # debug check:
                    #print(f"sub_data Generated")

                    time.sleep(5)


        data.append({
            "Abstract#": Abstract_Number, "Abstract Title":sub_session_title , "Date": session_date,
            "Time": session_time,
            "Location": session_loc, "URL": driver01.current_url, "Author": Author_name,
            "Author Affiliations": Author_affil, "Abstract text": Abstract_text,
            "Category": "", "sub-Category": "",
            "Session Title": session_title
        })
        # error Checking for data:
        # if(len(data)>2):
        #     print(data)
        driver01.back()
        # element.send_keys(Keys.COMMAND, Keys.ALT, Keys.ARROW_LEFT)
        time.sleep(10)

    # write into Json file
    with open("./data.json","w") as file:
        file.write(json.dumps(data))

    #writing into excel file
    pd.read_json("data.json").to_excel("output.xlsx")


    time.sleep(3)


function()
