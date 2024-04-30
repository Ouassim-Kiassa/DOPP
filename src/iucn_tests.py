import iucn_data

# use reduced data set for additional infos, only query stuff for animalia
country_occurrences_merged = iucn_data.get_merged_country_info().reset_index()
historical_info_merged = iucn_data.get_merged_historical_info().reset_index()
habitat_info_merged = iucn_data.get_merged_habitat_info().reset_index()
threats_info_merged = iucn_data.get_merged_threats_info().reset_index()
species_df = iucn_data.get_animalia_df().reset_index()

# print(species_df)
# print(species_df.columns)

#print(habitat_info_merged.loc[79934933])

# store filtered dataframe as csv (better for submitting assignment)
#iucn_data.save_df_as_csv(data_filtered, data_path, 'animalia.csv')

print(country_occurrences_merged.shape)
#print(country_occurrences_merged.head(50))
# get species (taxon_id) without country information
species_without_countries = list(set(species_df['taxonid_iucn'].unique()) - set(country_occurrences_merged['taxonid_iucn'].unique()))
print(f'Species without country occurrence: {len(species_without_countries)}')

print(historical_info_merged.shape)
#print(historical_info_merged.head(50))
# get species (taxon_id) without historical assessment information
species_without_hist_info = list(set(species_df['taxonid_iucn'].unique()) - set(historical_info_merged['taxonid_iucn'].unique()))
print(f'Species without hist info: {len(species_without_hist_info)}')

print(habitat_info_merged.shape)
#print(habitat_info_merged.head(50))
# get species (taxon_id) without habitat information
species_without_habitat_info = list(set(species_df['taxonid_iucn'].unique()) - set(habitat_info_merged['taxonid_iucn'].unique()))
print(f'Species without habitat info: {len(species_without_habitat_info)}')

print(threats_info_merged.shape)
# print(threats_info_merged.head(50))
# get species (taxon_id) without threats information
species_without_threats_info = list(set(species_df['taxonid_iucn'].unique()) - set(threats_info_merged['taxonid_iucn'].unique()))
print(f'Species without habitat info: {len(species_without_threats_info)}')
