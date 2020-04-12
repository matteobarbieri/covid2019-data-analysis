#!/usr/bin/env python
# coding: utf-8

# In[35]:

# In[36]:


import os, sys, glob


# In[37]:


import pandas as pd

import numpy as np

import seaborn as sns

import matplotlib.pyplot as plt

import matplotlib.ticker as ticker

import matplotlib.dates as mdates


# In[38]:


from datetime import datetime


# ### Required for google colab

# ### Setup

# In[39]:


DATA_DIR = "data-ita/dati-regioni"
# DATA_DIR = "../data-ita/dati-province"
PLOTS_DIR = "plots"


# ## Data loading

# In[40]:


csv_files = glob.glob(DATA_DIR + "/*-2020*.csv")


# In[41]:


def extract_date(file_name):

    # Sample file path:
    # '../data-ita/dati-regioni/dpc-covid19-ita-regioni-20200313.csv'

    # Remove file extension
    date_str = os.path.basename(file_name)[:-4]

    # Extract last 8 characters
    date_str = date_str[-8:]

    date = datetime.strptime(date_str, '%Y%m%d').date()

    return date


# In[42]:


country_df = None

for csv_file in csv_files:

    df = pd.read_csv(csv_file)
    date = extract_date(csv_file)
    df['Date'] = date

    if country_df is None:
        country_df = df
    else:
        country_df = pd.concat((country_df, df), ignore_index=True)


# In[43]:


np.unique(country_df['denominazione_regione'])


# In[44]:


country_df.head()


# In[45]:


def get_region_data(country_df, region_name):
    region_df = country_df[country_df['denominazione_regione'] == region_name].sort_values(by="Date").copy()

    region_df['casi_su_tamponi'] = region_df['totale_casi']/region_df['tamponi']

    region_df['numero_nuovi_casi'] = region_df['totale_casi'].diff()
    region_df['numero_nuovi_tamponi'] = region_df['tamponi'].diff()

    region_df['casi_su_tamponi_daily'] = region_df['numero_nuovi_casi']/region_df['numero_nuovi_tamponi']

    return region_df


# In[46]:


regions_list = [
    'Puglia',
    'Calabria',
    'Sicilia',
    'Campania',
    'Calabria',
#     'Lombardia',
]

# provinces_list = [
# #     'Lodi',
#     'Napoli',
# #     'Bari',
# ]


# In[47]:


ax = plt.gca()

sns.set_style("whitegrid", {'grid.linestyle': ':'})
# ax.yaxis.set_major_locator(ticker.MultipleLocator(Y_GRID_TICK))
ax.xaxis.set_major_locator(ticker.MultipleLocator(4))

for region_name in regions_list:
#     region_df = country_df[country_df['denominazione_regione'] == region_name]
    region_df = get_region_data(country_df, region_name)
    region_df.plot(x='Date', y=["nuovi_positivi"], figsize=(18,9), ax=ax, marker='o')


# region_df = country_df[country_df['denominazione_regione'] == 'Lombardia']
# region_df.plot(x='Date', y=["nuovi_attualmente_positivi"], figsize=(18,9), ax=ax, marker='o', secondary_y=True)

# for province_name in provinces_list:
#     province_df = country_df[country_df['denominazione_provincia'] == province_name]
#     province_df.plot(x='Date', y=["totale_casi"], figsize=(18,9), ax=ax, marker='o')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax.set_ylabel("# of confirmed cases");

ax.set_title("Daily numbers of confirmed cases, deaths and hospitalized people. Daily increase refers to numbers on the right y axis.");

# ax.legend(provinces_list)
# ax.legend(regions_list+['Lombardia'])
ax.legend(regions_list)

# plt.savefig("regions_daily_data.png");


# The 10 regions with the higher number of confirmed cases

# In[48]:


country_df.tail()


# In[49]:


latest_date = country_df['Date'].max()

top10_hit_regions = country_df[country_df['Date'] == latest_date]     .sort_values(by='totale_casi', ascending=False)     .head(10)['denominazione_regione']


# In[50]:


ax = plt.gca()

sns.set_style("whitegrid", {'grid.linestyle': ':'})
# ax.yaxis.set_major_locator(ticker.MultipleLocator(Y_GRID_TICK))
ax.xaxis.set_major_locator(ticker.MultipleLocator(4))

for region_name in top10_hit_regions:
#     region_df = country_df[country_df['denominazione_regione'] == region_name]
    region_df = get_region_data(country_df, region_name)
    region_df.plot(x='Date', y=["casi_su_tamponi"], figsize=(18,9), ax=ax, marker='o')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax.set_ylabel("Confirmed cases/tests performed ratio");

ax.set_title("Ratio of total confirmed cases over number of tests (10 hardest hit regions)");

ax.set_ylim([0, 0.5])

ax.legend(top10_hit_regions);

plt.savefig(os.path.join(PLOTS_DIR, "cases_over_tests_ratio_italy.png"));


# In[51]:


ax = plt.gca()

sns.set_style("whitegrid", {'grid.linestyle': ':'})
# ax.yaxis.set_major_locator(ticker.MultipleLocator(Y_GRID_TICK))
ax.xaxis.set_major_locator(ticker.MultipleLocator(4))

for region_name in regions_list:
#     region_df = country_df[country_df['denominazione_regione'] == region_name]
    region_df = get_region_data(country_df, region_name)
    region_df.plot(x='Date', y=["tamponi"], figsize=(18,9), ax=ax, marker='o')


# region_df = country_df[country_df['denominazione_regione'] == 'Lombardia']
# region_df.plot(x='Date', y=["nuovi_attualmente_positivi"], figsize=(18,9), ax=ax, marker='o', secondary_y=True)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax.set_ylabel("Confirmed cases/tests performed ratio");

ax.set_title("Total number of tests");

ax.legend(regions_list);

# plt.savefig("regions_daily_data.png");
