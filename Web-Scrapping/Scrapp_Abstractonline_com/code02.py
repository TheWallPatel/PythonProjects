import pandas as pd
import json
data = []
data.append({
            "Abstract#": 1, "Abstract Title":"sub_session_title" , "Date": "12-12-20",
            "Time": "12:20",
            "Location": "Moscow", "URL": "driver01.current_url", "Author": "Author_name",
            "Author Affiliations": "Author_affil", "Abstract text":" Abstract_text",
            "Category": "", "sub-Category": "",
            "Session Title": "session_title"
        })
data.append({
            "Abstract#": 1, "Abstract Title":"sub_session_title" , "Date": "12-12-20",
            "Time": "12:20",
            "Location": "Moscow", "URL": "driver01.current_url", "Author": "Author_name",
            "Author Affiliations": "Author_affil", "Abstract text":" Abstract_text",
            "Category": "", "sub-Category": "",
            "Session Title": "session_title"
        })


print(data)
with open("./data.json","w") as file:
    file.write(json.dumps(data))

pd.read_json("data.json").to_excel("output.xlsx")