import os
import time
import requests
from bs4 import BeautifulSoup
import mysql.connector

####################################################################################################################################
# Configuration via environment variables with safe defaults
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyCu_5lSQu2VxT7eHtpC9HH3cJuvD43tJZQ")
GOOGLE_CX = os.getenv("GOOGLE_CX", "f64288f4671ea43e1")
GOOGLE_CR = os.getenv("GOOGLE_CR", "in")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3307"))
DB_USER = os.getenv("DB_USER", "testuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "testpass")
DB_NAME = os.getenv("DB_NAME", "testdb")

ROLES = ["Data_Scientist", "Business_analyst", "Software_engineer"]


def get_mysql_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def fetch_links_for_roles(roles, max_results=100):
    all_links = []
    seen = set()
    session = requests.Session()
    for role in roles:
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX,
            "cr": GOOGLE_CR,
            "q": "jobs for " + role,
            "start": 0,
        }
        while params["start"] < max_results:
            try:
                response = session.get(
                    "https://www.googleapis.com/customsearch/v1",
                    params=params,
                    timeout=15,
                )
                payload = response.json()
            except Exception:
                break
            items = payload.get("items", [])
            if not items:
                break
            for item in items:
                url = item.get("link")
                if url and url not in seen:
                    seen.add(url)
                    all_links.append(url)
            params["start"] += 10
    return all_links


def build_skills_mapping():
    return {
        'airflow': 'Airflow', 'alteryx': 'Alteryx', 'asp.net': 'ASP.NET', 'atlassian': 'Atlassian',
        'excel': 'Excel', 'power bi': 'Power BI', 'power_bi': 'Power BI', 'tableau': 'Tableau', 'srss': 'SRSS', 'word': 'Word',
        'unix': 'Unix', 'linux/unix': 'Linux / Unix', 'linux': 'Linux', 'vue': 'Vue', 'jquery': 'jQuery', 'seaborn': 'Seaborn',
        'microstrategy': 'MicroStrategy', 'spss': 'SPSS', 'visio': 'Visio', 'gdpr': 'GDPR', 'ssrs': 'SSRS',
        'spreadsheet': 'Spreadsheet', 'aws': 'AWS', 'hadoop': 'Hadoop', 'ssis': 'SSIS',
        'sap': 'SAP', 'powerpoint': 'PowerPoint', 'sharepoint': 'SharePoint', 'redshift': 'Redshift',
        'snowflake': 'Snowflake', 'qlik': 'Qlik', 'cognos': 'Cognos', 'pandas': 'Pandas', 'spark': 'Spark', 'outlook': 'Outlook',
        'sql': 'SQL', 'python': 'Python', ' r ': 'R', 'javascript': 'JavaScript', 'js': 'JavaScript', 'java': 'Java',
        'scala': 'Scala', 'sas': 'SAS', 'matlab': 'MATLAB', 'c++': 'C++', 'c/c++': 'C / C++', 'perl': 'Perl',
        'typescript': 'TypeScript', 'bash': 'Bash', 'html': 'HTML', 'css': 'CSS', 'php': 'PHP', 'powershell': 'Powershell',
        'rust': 'Rust', 'kotlin': 'Kotlin', 'ruby': 'Ruby', 'dart': 'Dart', 'assembly': 'Assembly',
        'swift': 'Swift', 'vba': 'VBA', 'lua': 'Lua', 'groovy': 'Groovy', 'delphi': 'Delphi', 'objective-c': 'Objective-C',
        'haskell': 'Haskell', 'elixir': 'Elixir', 'julia': 'Julia', 'clojure': 'Clojure', 'solidity': 'Solidity',
        'lisp': 'Lisp', 'f#': 'F#', 'fortran': 'Fortran', 'erlang': 'Erlang', 'apl': 'APL', 'cobol': 'COBOL',
        'ocaml': 'OCaml', 'crystal': 'Crystal', 'javascript/typescript': 'JavaScript / TypeScript', 'golang': 'Golang',
        'nosql': 'NoSQL', 'mongodb': 'MongoDB', 't-sql': 'Transact-SQL', 'no-sql': 'No-SQL', 'visual basic': 'Visual Basic',
        'pascal': 'Pascal', 'mongo': 'Mongo', 'pl/sql': 'PL/SQL', 'sass': 'Sass', 'vb.net': 'VB.NET', 'mssql': 'MSSQL',
    }


def scrape_and_count_skills(links):
    skills_map = build_skills_mapping()
    result_counts = {"id": str(time.localtime().tm_yday) + str(time.localtime().tm_year)}
    session = requests.Session()
    index = 0
    for url in links:
        if url == "https://money.usnews.com/careers/best-jobs/data-scientist":
            continue
        try:
            response = session.get(url, timeout=15)
            index += 1
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text().lower()
            seen_on_page = set()
            for keyword, display in skills_map.items():
                if keyword in text_content and display not in seen_on_page:
                    result_counts[display] = result_counts.get(display, 0) + 1
                    seen_on_page.add(display)
        except Exception:
            continue
    return result_counts


def create_table_if_not_exists(cursor, table_name, keys):
    columns = []
    for key in keys:
        if key == "id":
            columns.append(f"`{key}` VARCHAR(32)")
        else:
            columns.append(f"`{key}` INT")
    query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join(columns)})"
    cursor.execute(query)


def insert_row(cursor, table_name, row_dict):
    columns = ", ".join(f"`{col}`" for col in row_dict.keys())
    placeholders = ", ".join(["%s"] * len(row_dict))
    sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(row_dict.values()))


def main():
    links = fetch_links_for_roles(ROLES, max_results=100)
    data = scrape_and_count_skills(links)

    # Ensure keys are strings and sorted for stable column ordering
    keys_sorted = sorted(str(k) for k in data.keys())
    ordered_data = {k: data[k] for k in keys_sorted}

    connection = get_mysql_connection()
    try:
        cursor = connection.cursor()
        table_name = "analysis"
        create_table_if_not_exists(cursor, table_name, ordered_data.keys())
        insert_row(cursor, table_name, ordered_data)
        connection.commit()
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        connection.close()


if __name__ == "__main__":
    main()










