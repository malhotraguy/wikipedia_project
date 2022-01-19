# https://dev.to/dmitryzub/how-to-scrape-google-knowledge-graph-with-python-2ilp
#https://medium.com/analytics-vidhya/the-two-google-search-python-libraries-you-should-never-miss-dfb2ec324a33
from time import sleep

from bs4 import BeautifulSoup
import requests, lxml
import re

headers = {
    'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def get_soup_from_query(query):
    print(f"query: {query}")
    html = requests.get(f'https://www.google.com/search?q={query}&hl=en', headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup


def get_from_knowledge_graph(query):
    soup = get_soup_from_query(query)
    for result in soup.select(".rVusze"):
        key_element = result.select_one(".w8qArf").text
        if result.select_one(".kno-fv"):
            value_element = result.select_one(".kno-fv").text.replace(": ", "")
        else:
            value_element = None
        if "population" in key_element.lower():
            return value_element


def get_google_result(city, query=None, max_retries=2):
    if query is None:
        query = f"{city} population"
    soup = get_soup_from_query(query)
    div_value = soup.find("div", {"class": "ayqGOc kno-fb-ctx KBXm4e"})
    if div_value is None:
        sleep(1)
        div_value = soup.find("div", {"class": "Z0LcW"})
    if div_value is not None:
        sleep(1)
        div_value_content = div_value.text
    else:
        sleep(1)
        div_value_content = get_from_knowledge_graph(city)
        if div_value_content is None:
            if max_retries == 0:
                return "0"
            else:
                max_retries -= 1
            sleep(2)
            return get_google_result(city=city, query=f"{city} population 2021", max_retries=max_retries)
        else:
            return div_value_content
    print(f"div_value_content: {div_value_content}")
    value_element = div_value_content.replace(u'\xa0', u' ')
    return value_element


def get_population(city):
    print(city)
    population = get_google_result(city=city)
    year_regex_search = re.search(r"\((\d{4})", population) or re.search(r"(\d{4})\)", population)
    if year_regex_search:
        year = year_regex_search.group(1)
    else:
        year = "2021"
    population = population.split("(")[0]
    population = population.strip()
    population = population.replace(",", "")
    if population.endswith("million"):
        population = population.split("million")[0]
        population = float(population) * 1000000
    print(f"Population Year: {year}")
    population = int(population)
    return population,int(year)


if __name__ == '__main__':
    city_population = get_population(city="Taipei")
    print(city_population)
