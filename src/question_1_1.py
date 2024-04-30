import iucn_data
import seaborn as sns
import geopandas
import matplotlib.pyplot as plt

animalia_df = iucn_data.get_animalia_df()
historical_df = iucn_data.get_merged_historical_info()

cat_cols = {
    "Lower Risk/least concern": "green",
    "Vulnerable": "lightblue",
    "Endangered": "darkred",
    "Critically Endangered": "indianred"
}

cat = ["Lower Risk/least concern", "Vulnerable", "Endangered", "Critically Endangered"]
df = historical_df.query(f'category in {cat}')
df = df.groupby(['year', 'category'], as_index=False).size()
sns.catplot(data=df, kind="bar",
            x='year', y='size', hue='category',
            height=6, aspect=3, palette=cat_cols, legend=False,
            hue_order=["Lower Risk/least concern", 'Vulnerable', 'Endangered',  "Critically Endangered"])
plt.xticks(rotation=45)
plt.legend(loc='center left',)
plt.ylabel('Assessments')
plt.title('Categorical Assessments in Year')
plt.tight_layout()
plt.show()
