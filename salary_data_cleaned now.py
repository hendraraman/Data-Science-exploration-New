# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 14:59:11 2023

@author: home
"""
# goal is to predict salary
import datetime
import pandas as pd

df = pd.read_csv("glassdoor_jobs.csv")
#print(df)
#removing rows where salary estimate is -1
df = df[df["Salary Estimate"] != "-1"]

# parsing through salary estimate
salary = df["Salary Estimate"].apply(lambda x: x.split("(")[0])
salary = salary.apply(lambda x: x.replace("$","").replace("K",""))
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)
final_sal = salary.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))
min_hr = final_sal.apply(lambda x: x.split("-")[0])
max_hr = final_sal.apply(lambda x: x.split("-")[1])
df['min_salary'] = min_hr.apply(lambda x: int(x))
df['max_salary'] = max_hr.apply(lambda x: int(x))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#making company name with only text
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3],axis = 1)

# state (location)
df['job_state'] = df['Location'].apply(lambda x : x.split(",")[1])
#print(df.job_state.value_counts())

# location is same as headquarters?
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0 ,axis =1 )

# finding the age of the company
    #getting current year from datetime library
year = datetime.date.today().year
df['age'] = df['Founded'].apply(lambda x: x if x < 1 else year-x)
 
# job descriptions
# python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()

# R-studio
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()

# spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()

# aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()

# excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()

# dropping first column
#axis = 1 specifies column
#print(df.columns)
df_final = df.drop(['Unnamed: 0'],axis = 1)
df_final.to_csv('salary_data_cleaned',index = False)