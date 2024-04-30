# source: https://www.gbif.org/dataset/19491596-35ae-4a91-9a98-85cf505f1bd3
import pandas as pd
import gbif_api as api

# from dwca.read import DwCAReader
# with DwCAReader('../data/iucn-2021-2.zip') as dwca:
#     # Check the core file of the Archive  (Occurrence, Taxon, ...)
#     print("Core type is: {}".format(dwca.descriptor.core.type))
#
#     # Check the available extensions
#     print("Available extensions: {}".format([ext.split("/")[-1] for ext in dwca.descriptor.extensions_type]))
#
#     taxon_df = dwca.pd_read('taxon.txt', low_memory=False)
#     descr_df = dwca.pd_read('distribution.txt', low_memory=False)
#     vern_df = dwca.pd_read('vernacularname.txt', low_memory=False)
#
# # Join the information of the description and vernacularname extension to the core taxon information
# # (cfr. database JOIN)
# taxon_df = pd.merge(taxon_df, descr_df, left_on='id', right_on='coreid', how="left")
# taxon_df = pd.merge(taxon_df, vern_df, left_on='id', right_on='coreid', how="left")

# constant
data_path = '../data/iucn_gbif'
dist_path = data_path + '/distribution.txt'
taxon_path = data_path + '/taxon.txt'
name_path = data_path + '/vernacularname.txt'

# distribution
distribution_df = pd.read_csv(dist_path, sep='\t', header=None, low_memory=False,
                              dtype={'coreid': 'string'},
                              names=['coreid', 'threatStatus', 'locality', 'source',
                                     'occurrenceStatus', 'establishmentMeans', 'countryCode'])
print(distribution_df.head(10))

# taxon
taxon_df = pd.read_csv(taxon_path, sep='\t', header=None, low_memory=False,
                       dtype={'coreid': 'string'},
                       names=['coreid', 'scientificName', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus',
                              'specificEpithet', 'scientificNameAuthorship', 'taxonRank', 'infraspecificEpithet',
                              'taxonomicStatus', 'acceptedNameUsageID', 'bibliographicCitation', 'references'])
print(taxon_df.head(10))

# vernacularname
name_df = pd.read_csv(name_path, sep='\t', header=None, low_memory=False,
                      dtype={'coreid': 'string'},
                      names=['coreid', 'language', 'vernacularName', 'isPreferredName'])
print(name_df.head(10))

print("DE SCHEISVIEHR")
vieher_df = pd.merge(taxon_df, distribution_df, on='coreid', how='inner')
vieher_df = pd.merge(vieher_df, name_df, on='coreid', how='left')
print(vieher_df.head(10))
print(vieher_df.columns)

# query for things we want:
param_threatStatus = ['Endangered', 'Critically Endangered']
param_kingdom = ['ANIMALIA']
query_string = "threatStatus in @param_threatStatus and kingdom == @param_kingdom"
vieher_df = vieher_df.query(query_string)

# get unique
u_id = vieher_df['coreid'].unique()
name_id = vieher_df['scientificName'].unique()

print(f'got {vieher_df.shape[0]} animals;'
      f'\n{len(u_id)} unique(per id)'
      f'\n{len(name_id)} unique(per name)')

# get tha fucking map
taxon_key = vieher_df.iloc[10]['coreid']
print(taxon_key)
api.get_map_for_taxonkey(212)
api.get_occurences_for_taxonkey(212)