from bs4 import BeautifulSoup
import requests
import pandas
from keywords import pracuj_job_keywords, pracuj_excluded_keywords
from urls import pracuj_urls


pracuj_job_info = []


def get_a_page_content(pracuj_url, no_page):
    url = pracuj_url.replace("{no_page}", str(no_page))
    pracuj_page = requests.get(url)
    soup = BeautifulSoup(pracuj_page.content, "html.parser")
    pracuj_jobs = soup.find_all("div", class_="c8i823f")
    return pracuj_jobs


def find_jobs():
    for pracuj_url in pracuj_urls:
        for no_page in range(1, 99):
            for pracuj_job in get_a_page_content(pracuj_url, no_page):
                pracuj_job_title = pracuj_job.find("h2", class_="b1iadbg8").text

                if any(any_part.lower() in pracuj_job_title.lower() for any_part in pracuj_job_keywords):
                    if any(any_part.lower() in pracuj_job_title.lower() for any_part in pracuj_excluded_keywords):
                        continue
                    else:
                        pracuj_job_company = pracuj_job.find("h4", "e1ml1ys4 t1c1o3wg").text
                        pracuj_job_link = pracuj_job.find("a", class_="bwcfwrp njg3w7p")["href"]
                    pracuj_job_info.append([pracuj_job_title, pracuj_job_company, pracuj_job_link])

    dataframe = pandas.DataFrame(pracuj_job_info, columns=["Job title", "Company", "Link to the offer"])
    dataframe.to_csv('saved offers.csv', encoding="utf16")

    print(f"Jobs offers saved on a file.")


if __name__ == "__main__":
    find_jobs()
