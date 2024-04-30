import iucn_data
import geopandas as pgd
import matplotlib.pyplot as plt


def fix_missing_codes(world):
    # just done because of an existing bug
    world2 = world.copy()

    world2.loc[world['name'] == 'France', 'iso_a3'] = 'FRA'
    world2.loc[world['name'] == 'Norway', 'iso_a3'] = 'NOR'
    world2.loc[world['name'] == 'Somaliland', 'iso_a3'] = 'SOM'
    world2.loc[world['name'] == 'Kosovo', 'iso_a3'] = 'RKS'
    return world2


world = pgd.read_file(pgd.datasets.get_path('naturalearth_lowres'))
world = fix_missing_codes(world)
# france is mapped wrongly
# world['iso_a3'] = world['iso_a3'].replace('-99', 'FRA')
world_min = world[['iso_a3', 'continent', 'geometry']]
animalia_df = iucn_data.get_animalia_df()
country_df = iucn_data.get_merged_country_info()

df = animalia_df.join(country_df, how='left')
df = df.drop('continent', axis=1)

df = df.merge(world_min, left_on='code_3', right_on='iso_a3', how='right')

print(df.continent.unique())


def df_to_plot(df_map, column_to_map, legend):
    ax = df_map.plot(column=column_to_map, cmap='OrRd', legend=True,
                     legend_kwds={'label': '', 'orientation': "horizontal"},
                     missing_kwds={'color': 'lightgrey'})
    ax.set_axis_off()
    plt.title(legend)
    plt.tight_layout()
    plt.show()


# only phylum - continent
phylum = ['CHORDATA', 'ARTHROPODA', 'MOLLUSCA']
df_p = df.query('phylum in @phylum')

# plot per continent
continent_count = df_p.groupby(['continent'], as_index=False).size()
df_2 = world_min.merge(continent_count)

df_to_plot(df_2, 'size', f'Species by Continent\n ({", ".join(phylum)})')

# plot per country
country_count = df.groupby(['iso_a3'], as_index=False).size()
df_2 = world_min.merge(country_count, how='left')
df_to_plot(df_2, 'size', f'Species by Country\n ({", ".join(phylum)})')

interesting_classes = ['INSECTA', 'AMPHIBIA', 'REPTILIA', 'MAMMALIA', 'AVES', 'ACTINOPTERYGII']
df_c = df.query('`class` in @interesting_classes')
country_count = df_c.groupby(['iso_a3'], as_index=False).size()
df_2 = world_min.merge(country_count, how='left')
df_to_plot(df_2, 'size', f'Species by Country\n ({", ".join(interesting_classes)})')

for cla in interesting_classes:
    df_ci = df.query('`class` == @cla')
    country_count = df_ci.groupby(['iso_a3'], as_index=False).size()
    df_2 = world_min.merge(country_count, how='left')
    df_to_plot(df_2, 'size', f'Species by Country\n ({cla})')