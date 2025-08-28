import requests
import time
import json
from bs4 import BeautifulSoup
import mysql.connector

####################################################################################################################################
mydb =  mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="testuser",
    password="testpass",
    database="testdb"
)

####################################################################################################################################
#--------------------the below code is to get first 10 search request links in google search using csj api-------------------------
roles=["Data_Scientist","Business_analyst","Software_engineer"]
for j in roles:
  params = {
  "key": "AIzaSyCu_5lSQu2VxT7eHtpC9HH3cJuvD43tJZQ",
  "cx": "f64288f4671ea43e1",
  "cr": "in",
  "q": "jobs for " + j,
  "start": 0
  }

links=[]
while(params["start"]<100):
   response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
   data =response.json()
   if "items" in data:
      links.extend([item['link'] for item in data['items']])
      params["start"]+=10
   else:
      break   

t = str(time.localtime().tm_yday)+str(time.localtime().tm_year)

print (links)

data={}
data["id"]=t
####################################################################################################################################
index = 0 
for i in links:
     if i == "https://money.usnews.com/careers/best-jobs/data-scientist":
        continue
     try:   
         print(index)
         response = requests.get(i)
         index += 1
         print('\\n')
         soup = BeautifulSoup(response.content, 'html.parser')
     #    soup_list = soup.find_all(['h1', 'h2', 'h3','p'])
     #    soup=BeautifulSoup(''.join(str(s) for s in soup_list), 'html.parser')
         keywords_skills = {
    'airflow': 'Airflow', 'alteryx': 'Alteryx', 'asp.net': 'ASP.NET', 'atlassian': 'Atlassian', 
    'excel': 'Excel', 'power_bi': 'Power BI', 'tableau': 'Tableau', 'srss': 'SRSS', 'word': 'Word', 
    'unix': 'Unix', 'vue': 'Vue', 'jquery': 'jQuery', 'linux/unix': 'Linux / Unix', 'seaborn': 'Seaborn', 
    'microstrategy': 'MicroStrategy', 'spss': 'SPSS', 'visio': 'Visio', 'gdpr': 'GDPR', 'ssrs': 'SSRS', 
    'spreadsheet': 'Spreadsheet', 'aws': 'AWS', 'hadoop': 'Hadoop', 'ssis': 'SSIS', 'linux': 'Linux', 
    'sap': 'SAP', 'powerpoint': 'PowerPoint', 'sharepoint': 'SharePoint', 'redshift': 'Redshift', 
    'snowflake': 'Snowflake', 'qlik': 'Qlik', 'cognos': 'Cognos', 'pandas': 'Pandas', 'spark': 'Spark', 'outlook': 'Outlook',
    'sql' : 'SQL', 'python' : 'Python', ',r,':'R',',r ':'R' ,' r ': 'R', ',c,':'C',' c ':'C', ',c ':'C', 'javascript' : 'JavaScript', 'js':'JS', 'java':'Java', 
    'scala':'Scala', 'sas' : 'SAS', 'matlab': 'MATLAB', 'c++' : 'C++', 'c/c++' : 'C / C++', 'perl' : 'Perl',
    'typescript' : 'TypeScript','bash':'Bash','html' : 'HTML','css' : 'CSS','php' : 'PHP','powershell' : 'Powershell',
    'rust' : 'Rust', 'kotlin' : 'Kotlin','ruby' : 'Ruby','dart' : 'Dart','assembly' :'Assembly',
    'swift' : 'Swift','vba' : 'VBA','lua' : 'Lua','groovy' : 'Groovy','delphi' : 'Delphi','objective-c' : 'Objective-C',
    'haskell' : 'Haskell','elixir' : 'Elixir','julia' : 'Julia','clojure': 'Clojure','solidity' : 'Solidity',
    'lisp' : 'Lisp','f#':'F#','fortran' : 'Fortran','erlang' : 'Erlang','apl' : 'APL','cobol' : 'COBOL',
    'ocaml': 'OCaml','crystal':'Crystal','javascript/typescript' : 'JavaScript / TypeScript','golang':'Golang',
    'nosql': 'NoSQL', 'mongodb' : 'MongoDB','t-sql' :'Transact-SQL', 'no-sql' : 'No-SQL','visual_basic' : 'Visual Basic',
    'pascal':'Pascal', 'mongo' : 'Mongo','sql':'Sql', 'pl/sql' : 'PL/SQL','sass' :'Sass', 'vb.net' : 'VB.NET','mssql' : 'MSSQL',
      }       
        
         text_content = soup.get_text().lower()
         r={}
         for keyword, name in keywords_skills.items():
           if keyword.lower() in text_content:
              if name in data and (name not in r):
                 data[name]+=1
              else :
                 r[name]=1
                 data[name]=1
     except Exception as e:
         print("Error:", e)

mycursor = mydb.cursor()

def create_table(table_name, data):
    keys = data
    columns = ', '.join([f"`{key}` VARCHAR(30)" for key in keys])
    query = f"CREATE TABLE {table_name} ({columns})"
    mycursor.execute(query)
    
s=list(data.keys())
for i in range(len(s)):
   s[i]=str(s[i])
s.sort()
print(s)

dat = {i: data[i] for i in s }

print(dat)

create_table("analysis", s)

columns =", ".join("`{}`".format(col) for col in dat.keys())
values = ", ".join(["%s"] * len(dat))
qry = "INSERT INTO "+j+" ({}) VALUES ({})".format(columns, values)
mycursor.execute(qry, list(dat.values()))
mydb.commit()
mycursor.close()
mydb.close()










