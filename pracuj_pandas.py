from bs4 import BeautifulSoup
import json
import requests
import pandas
from keywords import pracuj_job_keywords, pracuj_excluded_keywords, pracuj_desired_workplaces
from urls import pracuj_urls


pracuj_job_info = []


def unnest_nested_job_list(pracuj_job_offer_list, tag):
    for pracuj_job_offer_item in pracuj_job_offer_list:
        return pracuj_job_offer_item[tag]


def get_a_page_content(pracuj_url, no_page):
    url = pracuj_url.replace("{no_page}", str(no_page))
    pracuj_page = requests.get(url)
    soup = BeautifulSoup(pracuj_page.content, "html.parser")
    pracuj_jobs = soup.find("script", attrs={"id": "__NEXT_DATA__"}).text
    pracuj_jobs = json.loads(pracuj_jobs)
    pracuj_props = pracuj_jobs["props"]
    pracuj_pages_props = pracuj_props["pageProps"]
    pracuj_data_offers = pracuj_pages_props["data"]
    if pracuj_data_offers["jobOffers"]:
        pracuj_all_offers = pracuj_data_offers["jobOffers"]
        pracuj_grouped_offers = pracuj_all_offers["groupedOffers"]
        return pracuj_grouped_offers
    elif pracuj_data_offers["positionedJobOffers"]:
        pracuj_all_offers = pracuj_data_offers["positionedJobOffers"]
        pracuj_grouped_offers = pracuj_all_offers["groupedOffers"]
        return pracuj_grouped_offers


def find_jobs():
    for pracuj_url in pracuj_urls:
        for no_page in range(1, 99):
            for pracuj_job_offer in get_a_page_content(pracuj_url, no_page):
                pracuj_job_title = pracuj_job_offer["jobTitle"]

                if any(any_part.lower() in pracuj_job_title.lower() for any_part in pracuj_job_keywords):
                    pracuj_job_company = pracuj_job_offer["companyName"]
                    pracuj_job_offers_details = pracuj_job_offer["offers"]
                    pracuj_job_workplace = unnest_nested_job_list(pracuj_job_offers_details, "displayWorkplace")

                    if any(any_part.lower() in pracuj_job_title.lower() for any_part in pracuj_excluded_keywords):
                        continue

                    if any(any_part.lower() in pracuj_job_workplace.lower() for any_part in pracuj_desired_workplaces):
                        pracuj_job_link = unnest_nested_job_list(pracuj_job_offers_details, "offerAbsoluteUri")
                        pracuj_job_info.append([pracuj_job_title, pracuj_job_company, pracuj_job_workplace, pracuj_job_link])

    dataframe = pandas.DataFrame(pracuj_job_info, columns=["Job title", "Company", "Workplace", "Link to the offer"])
    dataframe.to_csv('saved offers.csv', encoding="utf16")

    print(f"Job offers saved on a file.")


if __name__ == "__main__":
    find_jobs()
