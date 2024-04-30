import iucn_data
import matplotlib.pyplot as plt

# check for missing values, data types and so on
animalia_df = iucn_data.get_animalia_df()
historical_df = iucn_data.get_merged_historical_info()
threats_df = iucn_data.get_merged_threats_info()
habitat_df = iucn_data.get_merged_habitat_info()
countries_df = iucn_data.get_merged_country_info()

def print_missing_values_summary(df, title):
    print(f"\n\nEvaluation of missing values for {title}:")
    # number of missing values in total
    nr_missing_values = df.isna().sum()
    print(nr_missing_values[nr_missing_values > 0])

    if nr_missing_values[nr_missing_values > 0].size != 0:
        nr_missing_values[nr_missing_values > 0].plot.bar()
        plt.xlabel("Column")
        plt.ylabel("Number of Missing Values")
        plt.title(f"Missing values for all columns - {title}")
        plt.gcf().subplots_adjust(bottom=0.4)
        plt.show()
    else:
        print(f'No missing values for {title}')

print("\nAnimal Data - Datatypes/Dataframe-Information:")
print(animalia_df.info())

print("\nHistorical Assessment Data - Datatypes/Dataframe-Information:")
print(historical_df.info())

print("\nThreats Data - Datatypes/Dataframe-Information:")
print(threats_df.info())

print("\nHabitat Data - Datatypes/Dataframe-Information:")
print(habitat_df.info())

print("\nCountry Occurrence Data - Datatypes/Dataframe-Information:")
print(countries_df.info())

# => statistical information (mean, std, etc.) does not make sense for this data

print_missing_values_summary(animalia_df, "Animal Data")
print_missing_values_summary(historical_df, "Historical Assessment Data")
print_missing_values_summary(threats_df, "Threats Data")
print_missing_values_summary(habitat_df, "Habitat Data")
print_missing_values_summary(countries_df, "Country Occurrence Data")

# no real outlier handling possible
# -> missing values could be only manually fixed

print(historical_df[historical_df.isnull().any(axis=1)])