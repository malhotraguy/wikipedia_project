# Population source : https://worldpopulationreview.com/world-cities

import wikipedia
import pandas as pd  # library for data analysis
import requests  # library to handle requests
from bs4 import BeautifulSoup  # library to parse HTML documents
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from google_test import get_population


def get_correct_number(population):
    population = population.strip()
    population = population.replace(",", "")
    if population.endswith("million"):
        population = population.split("million")[0]
        population = float(population) * 1000000
    population = int(population)
    return population


if __name__ == '__main__':
    name = 'List_of_most-visited_museums'
    # Use a breakpoint in the code line below to debug your script.
    # pprint(wikipedia.summary(f"{name}"))  # Press Ctrl+F8 to toggle the breakpoint.
    # print(wikipedia.page(f"{name}").links)
    # print(wikipedia.page(f"{name}").url)
    # print(wikipedia.page(f"{name}").categories)
    # print(wikipedia.page(f"{name}").html())
    # parse data from the html into a beautifulsoup object
    table_class = "wikitable sortable jquery-tablesorter"
    soup = BeautifulSoup(wikipedia.page(f"{name}").html(), 'html.parser')
    html_data_table = soup.find('table', {'class': "wikitable"})
    # print(html_data_table)
    data_list = pd.read_html(str(html_data_table))
    # convert list to dataframe
    data_df = pd.DataFrame(data_list[0])
    if "Image" in data_df.columns:
        data_df.drop(['No.', "Image"], axis=1, inplace=True)

        data_df.rename(columns={"Country and city": "City", "Visitors annually[a]": "Visitors per year"}, inplace=True)
        data_df[["Visitors per year", "Year Reported"]] = data_df["Visitors per year"].str.split("(",
                                                                                                 expand=True,
                                                                                                 n=1)
        data_df[["Year Reported", "Growth"]] = data_df["Year Reported"].str.split("\)\(",
                                                                                  expand=True,
                                                                                  n=1)
        data_df["Visitors per year"] = data_df["Visitors per year"].apply(
            lambda no_of_visitors: get_correct_number(population=no_of_visitors))
    else:
        data_df.rename(columns={"Country flag, city": "City"}, inplace=True)
        data_df["Year reported"] = data_df["Year reported"].map(lambda year: year.split("[")[0])

    data_df["Population"] = data_df["City"].apply(lambda city: get_population(city=city))
    data_df[["Population", "Population Reported Year"]] = data_df["Population"].str.split(",", expand=True, n=1)
    # print(data_df.head())
    # population_df = pd.read_csv("./cities_population.csv")
    # population_df.rename(columns={"Name": "City"}, inplace=True)
    # population_df.drop(['Prev'], axis=1, inplace=True)
    # merged_df = data_df.merge(population_df, how='inner', on=['City'])
    # merged_df.sort_values(by="rank", inplace=True, ignore_index=True)
    plt.scatter(data_df['Population'], data_df['Visitors per year'])
    plt.show()

    # assign X and Y
    x = data_df['Population'].values  # independent variable
    y = data_df['Visitors per year'].values  # dependent variable
    # sckit-learn implementation

    # Model initialization
    regression_model = LinearRegression()
    # Expected 2D array, so converting 1D array to 2D:
    x = x.reshape(-1, 1)
    # Fit the data(train the model)
    regression_model.fit(x, y)
    # Predict
    y_predicted = regression_model.predict(x)

    # model evaluation
    rmse = mean_squared_error(y, y_predicted)
    r2 = r2_score(y, y_predicted)

    # printing values
    print('Slope:', regression_model.coef_)
    print('Intercept:', regression_model.intercept_)
    print('Root mean squared error: ', rmse)
    print('R2 score: ', r2)

    # plotting values

    # data points
    plt.scatter(x, y, s=10)
    plt.xlabel('x')
    plt.ylabel('y')

    # predicted values
    plt.plot(x, y_predicted, color='r')
    plt.show()
