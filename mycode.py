# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 07:34:12 2022

@author: home
"""

import pandas as pd
df = pd.read_csv("C:/Hendra/learn/ds_salary_proj/glassdoor_jobs.csv")
df = df[df["Salary Estimate"] != "-1"]

#salary parsing
df ["hourly"] = df["Salary Estimate"].apply(lambda x: 1 if "per hour" in x.lower() else 0)   
df ["employee provider"] = df["Salary Estimate"].apply(lambda x: 1 if "employer provided salary" in x.lower() else 0)

salary = df["Salary Estimate"].apply(lambda x : x.split("(")[0])
#print("salary is",salary)

minus = salary.apply(lambda x: x.replace("K","").replace("$",""))
#print("minus is ",minus)
minimum = minus.apply(lambda x: x.lower().replace("employer provided salary:","").replace("per hour",""))
df ["min_salary"] = minimum.apply(lambda x: int(x.split("-")[0]))
df ["max_salary"] = minimum.apply(lambda x: int(x.split("-")[1]))
df ["avg_salary"] = (df["min_salary"]+df["max_salary"])/2

#company name text only
df["company_txt"] = df.apply(lambda x: x["Company Name"] if x["Rating"] <0 else x["Company Name"][:-3],axis = 1)

#state field
df["job_state"] = df["Location"].apply(lambda x: x.split(",")[1])

df["same_state"] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0 ,axis = 1)

#age of the company
current = 2022
df["age"] = df.Founded.apply(lambda x: 1 if x < 1 else current - x ) 

# parsing of job descriprion sucn as python, R, Excel

df["python_yn"] = df["Job Description"].apply(lambda x: 1 if "python" in x.lower() else 0)

df["R_yn"] = df["Job Description"].apply(lambda x: 1 if "r-studio" in x.lower() or  "r studio" in x.lower() else 0)

df["spark"] = df["Job Description"].apply(lambda x: 1 if "spark" in x.lower() else 0)

df["aws"] = df["Job Description"].apply(lambda x: 1 if "aws" in x.lower() else 0)

df["excel"] = df["Job Description"].apply(lambda x: 1 if "excel" in x.lower() else 0)

df_out = df.drop(["Unnamed: 0"],axis = 1)
df_out.to_csv("salary_data_cleaned.csv",index= False)

