import pandas as pd  # library for data analysis
import requests  # library to handle requests
from bs4 import BeautifulSoup  # library to parse HTML documents

# get the response in the form of html
from google_test import get_population

wikiurl = "https://en.wikipedia.org/wiki/List_of_most-visited_museums"
table_class = "wikitable sortable"
response = requests.get(wikiurl)


def get_correct_number(population):
    population = population.strip()
    population = population.replace(",", "")
    if population.endswith("million"):
        population = population.split("million")[0]
        population = float(population) * 1000000
    population = int(population)
    return population


# parse data from the html into a beautifulsoup object
soup = BeautifulSoup(response.text, 'html.parser')
html_data_table = soup.find('table', {'class': "wikitable"})
# print(html_data_table)
data_list = pd.read_html(str(html_data_table))
# convert list to dataframe
data_df = pd.DataFrame(data_list[0])
# print(data_df.head())
data_df["Year reported"] = data_df["Year reported"].map(lambda x: x.split("[")[0])
data_df.rename(columns={"Country flag, city": "City"}, inplace=True)
data_df["freq"] = data_df.groupby("City")["City"].transform('count')
population_df = pd.read_csv("./cities_population.csv")
population_df.rename(columns={"Name": "City"}, inplace=True)
population_df.drop(['Prev'], axis=1, inplace=True)
population_df.drop_duplicates(subset="City", inplace=True)
merged_df = data_df.merge(population_df, how='inner', on='City', indicator=True, validate="m:1")
merged_df.sort_values(by="rank", inplace=True, ignore_index=True)
# for city in data_df["City"]:
#     print(city)
#     city_population = get_population(city=city)
#     print(city_population)
data_df["Population"] = data_df["City"].apply(lambda x: get_population(city=x))
