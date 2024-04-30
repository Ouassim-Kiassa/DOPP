import iucn_data
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# constants
show_plots = True
common_phyla_names = {
    'CHORDATA': 'Chordates',
    'ARTHROPODA': 'Arthropods',
    'MOLLUSCA': 'Mollusks',
    'CNIDARIA': 'Cnidarians',
    'ANNELIDA': 'Segmented worms',
    'ECHINODERMATA': 'Echinoderms',
    'ONYCHOPHORA': 'Velvet worms',
    'NEMERTINA': 'Ribbon worms'
}

animalia_df = iucn_data.get_animalia_df()

# columns
# ['scientific_name', 'subspecies', 'rank', 'subpopulation',
#        'threatCategory', 'kingdom', 'phylum', 'class', 'order', 'family',
#        'genus', 'main_common_name', 'authority', 'published_year',
#        'assessment_date', 'category', 'criteria', 'population_trend',
#        'marine_system', 'freshwater_system', 'terrestrial_system', 'assessor',
#        'reviewer', 'aoo_km2', 'eoo_km2', 'elevation_upper', 'elevation_lower',
#        'depth_upper', 'depth_lower', 'errata_flag', 'errata_reason',
#        'amended_flag', 'amended_reason']
# print(animalia_df.columns)
# print(animalia_df.head(20))

# How many species are endangered?
count_overall = animalia_df['scientific_name'].nunique()
print(f"There are {count_overall} endangered species in total.")

# critical endangered
count_cr = animalia_df[animalia_df['threatCategory'] == 'CR']['scientific_name'].nunique()
print(f"Thereof are {count_cr} critical endangered.")

# endangered
count_en = animalia_df[animalia_df['threatCategory'] == 'EN']['scientific_name'].nunique()
print(f"Thereof are {count_en} endangered.")

# PIE CHART
# define data
df = animalia_df.groupby('threatCategory').size().reset_index(name='counts')

labels = ['Critical Endangered', 'Endangered']

if show_plots:
    fig = px.pie(df, values='counts', names=labels,
                 title='Breakdown of endangered and critical endangered species',
                 color_discrete_sequence=["indianred", "darkred"])
    fig.show()

    plt.pie(df['counts'], labels=labels, autopct='%.0f%%', colors=["darkred", "indianred"], startangle=90)
    # plt.legend(title="Threat Status", loc="upper left")
    plt.title('Breakdown of endangered and critical endangered species')
    plt.show()

# How many animals are endangered for a certain class (taxonomic rank; e.g., Mammalia)?

# by subphylum
df = animalia_df.groupby('phylum').size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
df['phylum'] = df['phylum'].map(common_phyla_names)
print(df)

df_bar_gen = animalia_df.groupby(['phylum', 'class'])['scientific_name'].count().to_frame()
df_bar_gen.sort_values(by=['phylum', 'scientific_name'], ascending=[True, False], inplace=True)
df_bar_gen.columns = ['counts']
df_bar_gen = df_bar_gen.reset_index()
print(df_bar_gen)
fig = px.bar(df_bar_gen, x='counts', y='class', color='phylum', text_auto='s', orientation='h', width=1000, height=1600)
fig.show()

if show_plots:
    fig = px.pie(df, values='counts', names='phylum',
                 title='Breakdown of endangered species by Phylum')
    fig.show()

    plt.pie(df['counts'], labels=df['phylum'].unique(), autopct='%.0f%%', startangle=90)
    # plt.legend(title="Phylum", bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=2)
    plt.title('Breakdown of endangered species by Phylum')
    plt.show()

# most interesting Phylum categories: Chordates, Arthropods, Mollusks
interesting_cat = ['CHORDATA', 'ARTHROPODA', 'MOLLUSCA']
df_red = animalia_df.query('phylum in @interesting_cat')
df_red = df_red.groupby(['phylum', 'class'])['scientific_name'].count().to_frame()
df_red.sort_values(by=['phylum', 'scientific_name'], ascending=[True, False], inplace=True)
df_red.columns = ['counts']
print(df_red)

df_bar = df_red.reset_index()
print(df_bar)
fig = px.bar(df_bar, x='counts', y='class', color='phylum', orientation='h', width=1000, height=1600, text_auto='s')
fig.show()

df_p = animalia_df.query('phylum in @interesting_cat').groupby(['phylum', 'class']) \
    .size().reset_index(name='counts') \
    .sort_values(by=['phylum', 'counts'], ascending=[True, False])

if show_plots:
    for cat in interesting_cat:
        fig = px.pie(df_p[df_p['phylum'] == cat], values='counts', names=df_p[df_p['phylum'] == cat]['class'].unique(),
                     title=f'% of {cat}')
        fig.show()

        plt.pie(df_p[df_p['phylum'] == cat]['counts'], labels=df_p[df_p['phylum'] == cat]['class'].unique(),
                autopct='%1.0f%%', startangle=90)
        plt.title(f'% of {cat}')
        plt.show()

# widely known animal classes are INSECTA, AMPHIBIA, REPTILIA, MAMMALIA, AVES (birds), ACTINOPTERYGII (ray-finned fish, which includes most familiar bony fish)
# how much of the total number of endangered animals are one of these classes
df_c = animalia_df.groupby(['class', 'threatCategory'])['scientific_name'].count().to_frame()
df_c.columns = ['counts']
print(df_c)

if show_plots:
    df_cr_plt = df_c.reset_index()

    f, ax = plt.subplots(figsize=(10, 15))
    sns.barplot(x='counts', y='class', hue='threatCategory', data=df_cr_plt,
                palette=["darkred", "indianred"],
                capsize=0.05,
                saturation=8
                )
    ax.legend(ncol=2, loc='lower right')
    plt.title('Breakdown of endangered species by Class and Threat Category')
    plt.gcf().subplots_adjust(left=0.25)
    plt.show()

# focus on those with interesting class
interesting_classes = ['INSECTA', 'AMPHIBIA', 'REPTILIA', 'MAMMALIA', 'AVES', 'ACTINOPTERYGII']
df_c_red = df_c.reset_index().query('`class` in @interesting_classes')
df_c_red_ind = df_c_red.set_index(['class', 'threatCategory'])
print(df_c_red_ind)

if show_plots:
    sns.barplot(x='counts', y='class', hue='threatCategory', data=df_c_red,
                palette=["darkred", "indianred"],
                capsize=0.05,
                saturation=8
                )
    plt.title('Breakdown of endangered species by Class and Threat Category')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
    plt.gcf().subplots_adjust(left=0.25)
    plt.show()


## how did it change over time?
hist_df = iucn_data.get_merged_historical_info().reset_index()
cat = ["Endangered", "Critically Endangered", "Vulnerable"]
label_mapping = {"Critically Endangered":"CR", "Endangered":"EN", "Vulnerable":"VU"}
cat_cols = ["indianred", "lightblue", "darkred"]
df = hist_df.query(f'category in {cat}')

df['category'] = df['category'].map(label_mapping)

df = df.groupby(['taxonid_iucn', 'category'])['year'].min().reset_index()
df = df.groupby(['year', 'category']).count()
df.columns = ['counts']

df['no_csum'] = df.groupby(['category'])['counts'].cumsum()

sns.lineplot(x='year', y='no_csum', hue='category', palette=cat_cols, data=df)
plt.show()

df_splt = df.reset_index()
sns.catplot(
    data=df_splt, kind="bar",
    x="year", y="no_csum", hue="category", palette=cat_cols, height=6
)
plt.xticks(rotation=90)
plt.show()