import requests
import csv
from bs4 import BeautifulSoup

# Returns the job position input
def get_position(position: str):
    return input("What position are you seeking? ")

# Returns the job location input
def get_location(location: str):
    return input("Where are you seeking that position? ")

# Returns the url of site based on position and location input
def get_url(position: str, location: str):
    url_template = "https://www.indeed.com/jobs?q={}&l={}&"
    url = url_template.format(position, location)
    return url

# Scrapes through job_title, company, location, job_description, post_date, salary, and posting_url and appends them into an array
def get_info(post):
    job_title = post.find("h2", "jobTitle", "title").text.strip()
    company = post.find("span", "companyName").text.strip()
    location = post.find("div", "companyLocation").text.strip()
    job_description = post.find("div", "job-snippet").text.strip()
    post_date = post.find("span", "date").text.strip()
    try:
        salary = post.find("span", "estimated-salary").text.strip()
    except:
        salary = ""
    post_url = post.find("a", "jcs-JobTitle").get("href")
    posting_url = "https://www.indeed.com" + post_url
    info = [job_title, company, location, job_description, post_date, salary, posting_url]
    return info

def main(position: str, location: str):
    # Initializing varibales
    infos = []
    position = get_position(position)
    location = get_location(location)
    url = get_url(position, location)

    while True:
        page = requests.get(url)
        full_page = BeautifulSoup(page.text, "html.parser")
        posts = full_page.find_all("div", "slider_item")

        for post in posts:
            info = get_info(post)
            infos.append(info)
        # While loop continues to run until there are no more pages left in the job search
        try:
            url = 'https://www.indeed.com' + full_page.find("a", {"aria-label": "Next"}).get("href")
            infos.append[url]
        except AttributeError:
            break
    # Creates csv of job scraping 
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["job_title", "company", "location", "job_description", "post_date", "salary", "post_url"])
        writer.writerows(infos)

main('','')