from bs4 import BeautifulSoup
import requests
import pandas


pracuj_job_info = []

pracuj_urls = [
    "https://www.pracuj.pl/praca/ma%C5%82opolskie;r,6/ostatnich%207%20dni;p,7?pn={no_page}&tc=0&ws=0&wm=full-office%2Chybrid%2Chome-office",
    "https://www.pracuj.pl/praca/mazowieckie;r,7/ostatnich%207%20dni;p,7?et=1%2C3%2C17%2C4&pn={no_page}&tc=0&ws=0&wm=hybrid%2Chome-office",
    "https://www.pracuj.pl/praca/wroclaw;wp/ostatnich%207%20dni;p,7/praca%20zdalna;wm,home-office?rd=0&et=1%2C3%2C17%2C4&pn={no_page}&tc=0&ws=0",
]

pracuj_job_keywords = [
    "data",
    "analyst",
    "analityk",
    "business",
    "python",
    "database",
    "baz danych",
    "product",
]

pracuj_excluded_keywords = [
    "senior",
    "starszy",
    "german",
    "italian",
    "czech",
    "portuguese",
    "dutch",
    "french",
    "turkish",
    "bulgarian",
    "lithuanian",
    "latvian",
    "russian",
    "finnish",
    "danish",
    "norwegian",
    "swedish",
    "niemiecki",
    "francuski",
    "rosyjski",
    "romanian",
    "hr ",
    " hr ",
    "sr "
    " sr ",
    "manager",
    "head",
    "kierownik",
    "graduate programme",
    "graduate",
    "production",
    "machine learning",
    "spark",
    "java",
    "lead",
    "doświadczon",
    "doświadczeni",
    "gcp",
    "react",
    "cloud",
    "power platform",
    " rpa ",
    "rpa ",
    " rpa",
    "tableau",
    "qlik",
    "django",
    "fullstack",
    "full stack",
    "oracle",
    "3d",
    "ecommerce",
    "US hours",
    "helpdesk",
    "help desk",
    "service desk",
    "sharepoint",
    "share point",
]


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