import time

from selenium import webdriver as driver00
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import json
import time

def check_element_exists(driver11,by_value, search_value):
    try:
        driver11.find_element(by_value,search_value)
    except NoSuchElementException:
        return False
    return True

def function():
    data = []
    driver01 = driver00.Chrome("./chromedriver.exe")

    driver01.get("https://www.naukri.com/")
    time.sleep(5)

    site = driver01.find_element_by_class_name("qsb")
    skill_search_class = site.find_element_by_class_name("keywordSugg")
    skill_Exper_class = site.find_element_by_class_name("qsbExperience")
    skill_Location_class = site.find_element_by_class_name("locationSugg")
    Submit_button = site.find_element_by_class_name("qsbSubmit")

    Skill_value_tag = skill_search_class.find_element_by_tag_name("input")
    Skill_value_tag.send_keys("Embedded System")

    skill_exper_tag = skill_Exper_class.find_element_by_tag_name("input")
    skill_exper_tag.send_keys("2 years")

    skill_location_tag = skill_Location_class.find_element_by_tag_name("input")
    skill_location_tag.send_keys("Pune")

    Submit_button.click()
    # driver01.pa
    time.sleep(5)

    list = driver01.find_element_by_class_name("list")
    article_list = list.find_elements_by_tag_name("article")

    for i in range(len(article_list)):
        job_title_class = article_list[i].find_element_by_class_name("jobTupleHeader")
        job_requirement_tag = article_list[i].find_element_by_class_name("has-description")
        job_footer_class = article_list[i].find_element_by_class_name("mt-20")

        # job title data:
        job_info_class = job_title_class.find_element_by_class_name("info")
        title_tag = job_info_class.find_element_by_class_name("title")
        Job_title = title_tag.text

        #company name:
        subTitle_tag = job_title_class.find_element_by_tag_name("div")
        company_name_tag = subTitle_tag.find_element_by_class_name("subTitle")
        company_name = company_name_tag.text

        star_rating = ""

        # if (subTitle_tag.find_element(By.CLASS_NAME, ("starRating")).is_displayed() &
        #         subTitle_tag.find_element_by_class_name(By.CLASS_NAME, ("reviewsCount")).is_displayed()):
        # print("company name search done")
        # making Rating and Review "" initially,
        reviews =""
        star_rating = ""
        if(check_element_exists(subTitle_tag,By.CLASS_NAME,"starRating") &
            check_element_exists(subTitle_tag,By.CLASS_NAME,"reviewsCount")):
            star_rating_tag = subTitle_tag.find_element_by_class_name("starRating")
            star_rating  = star_rating_tag.text

            reviews_tag = subTitle_tag.find_element_by_class_name("reviewsCount")
            reviews = reviews_tag.text

        ul_list_tag = job_info_class.find_element_by_tag_name("ul")
        ul_list = ul_list_tag.find_elements_by_tag_name("li")
        # for exp , salary, location
        exp_required = ""
        salary_offer = ""
        location = ""
        for ul_list00 in range(len(ul_list)):
            # for experience
            if ul_list00 == 0:
                # ex_li_tag = ul_list[0].find_element_by_class_name("experience")
                ex_li_tag = ul_list[0].find_element_by_tag_name("span")
                exp_required = ex_li_tag.text
                # print(exp_required)
            if ul_list00 == 1:
                # salary_li_tag = ul_list[1].find_element_by_class_name("salary")
                salary_li_tag = ul_list[1].find_element_by_tag_name("span")
                salary_offer = salary_li_tag.text
            if ul_list00 == 2:
                # location_li_tag = ul_list[2].find_element_by_class_name("location")
                location_li_tag = ul_list[2].find_element_by_tag_name("span")
                location = location_li_tag.text
        # Job requirement description
        job_requirement_list = job_requirement_tag.find_elements_by_tag_name("li")
        job_requirements = ""
        for li in job_requirement_list:
            job_requirements = job_requirements + str(",") + str(li.text)

        # job footer
        job_date = job_footer_class.find_element_by_class_name("type").find_element_by_tag_name("span").text

        # data.append([{
        #     "hello": "dhawal"
        # }])
        data.append({
            "number" : i,
            "title" : Job_title,
            "Requirement": job_requirements,
            "company": company_name,
            "reviews": star_rating,
            "reviewsCount":  reviews,
            "yrExp": exp_required ,
            "salary":salary_offer,
            "location" :location,
            "PostDate":job_date

        })
    print(data)
    with open("data.json","w") as file:
        file.write(json.dumps(data))

    pd.read_json("./data.json").to_excel("output.xlsx")


function()
