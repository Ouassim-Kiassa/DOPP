DOPP

# todo
- [ ] define global seaborn plot-theme
  - [ ] Map colors to categorize (e.g. critically endangered as red etc.)

# Data preparation(s)
there are 4 distinct data-sets callable with functions in `iucn_data.py`
- info about county's: `get_merged_country_info()`
- infos about historical assessment: `get_merged_historical_info()`
- infos about habitats: `get_merged_habitat_info()`
- list of species considered in the exercise (e.g. endangered and of kingdom animalia): `get_merged_habitat_info()`

in iucn_data (the dfs above) the `taxonid_iucn` is set as index, e.g. you can query an id via `habitat_info_merged.loc[79934933]`.


# Question 1:
in file `question_1.py`

## How many endangered species are there?
taxonomies classes: Kingdom->Phylum -> Class -> Order ->Family -> Genus -> Species