#Author: Rogelio Delgado
#Assignment 5-6
#Motor Vehicle Collisions - Crashes--- Source: https://catalog.data.gov/dataset/motor-vehicle-collisions-crashes


#Visual 1: 2012-2024 Number of Injuries by Category and City
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/Rogelio/OneDrive/Regis/MSDS 670/Week_5/mvc.csv")

injury_by_borough = df.groupby('BOROUGH').agg({
    'NUMBER OF PERSONS INJURED': 'sum',
    'NUMBER OF PEDESTRIANS INJURED': 'sum',
    'NUMBER OF CYCLIST INJURED': 'sum',
    'NUMBER OF MOTORIST INJURED': 'sum',
}).reset_index()

fig, ax = plt.subplots(figsize=(14, 8))

index = np.arange(len(injury_by_borough['BOROUGH']))
bar_width = 0.2

ax.bar(index, injury_by_borough['NUMBER OF PERSONS INJURED'], bar_width, label='Persons Injured')
ax.bar(index + bar_width, injury_by_borough['NUMBER OF PEDESTRIANS INJURED'], bar_width, label='Pedestrians Injured')
ax.bar(index + 2*bar_width, injury_by_borough['NUMBER OF CYCLIST INJURED'], bar_width, label='Cyclists Injured')
ax.bar(index + 3*bar_width, injury_by_borough['NUMBER OF MOTORIST INJURED'], bar_width, label='Motorists Injured')

ax.set_xlabel('Borough')
ax.set_ylabel('Number of Injuries (Thousands)')
ax.set_title('2012-2024 Number of Injuries by Category and Borough')
ax.set_xticks(index + bar_width + bar_width/2)
ax.set_xticklabels(injury_by_borough['BOROUGH'], rotation=0)
ax.legend()
ax.grid(False)

ticks = ax.get_yticks()
new_ticks = [str(int(x / 1000)) for x in ticks if x >= 20000 and x <= 140000]
ax.set_yticklabels(new_ticks)

plt.show()

###############################################################################

#Visual 2: Number of Collisions Over Time for the Last 8 Years
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/Rogelio/OneDrive/Regis/MSDS 670/Week_5/mvc.csv")

df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'])

df = df[(df['CRASH DATE'].dt.year >= 2017) & (df['CRASH DATE'].dt.year <= 2024)]

collisions_over_years = df.groupby([df['CRASH DATE'].dt.year, df['CRASH DATE'].dt.month]).size()
collisions_over_years_unstacked = collisions_over_years.unstack(level=0)

fig, ax = plt.subplots(figsize=(14, 8))

collisions_over_years_unstacked.plot(ax=ax, linewidth=3)

ax.set_title('Number of Collisions for Years 2017-2024')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Collisions')
ax.legend(title='Year', labels=[str(year) for year in sorted(df['CRASH DATE'].dt.year.unique(), reverse=True)])
ax.set_xticks(range(1,13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.show()

###############################################################################

#Visual 3:
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/Rogelio/OneDrive/Regis/MSDS 670/Week_5/mvc.csv")

df_filtered = df[df['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified']

top_vehicle_types = df_filtered['VEHICLE TYPE CODE 1'].value_counts().head(5).index
top_contributing_factors = df_filtered['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().head(7).index

filtered_df = df_filtered[df_filtered['VEHICLE TYPE CODE 1'].isin(top_vehicle_types) & 
                          df_filtered['CONTRIBUTING FACTOR VEHICLE 1'].isin(top_contributing_factors)]

cross_tab = pd.crosstab(filtered_df['VEHICLE TYPE CODE 1'], filtered_df['CONTRIBUTING FACTOR VEHICLE 1'])

cell_text_size = 20
ticks_size = 20
title_size = 24
colorbar_label_size = 16

fig, ax = plt.subplots(figsize=(20, 16))
cax = ax.matshow(cross_tab, cmap='coolwarm')

ax.set_title('Incident Counts by Vehicle Type and Contributing Factor', pad=20, fontsize=title_size)

cbar = plt.colorbar(cax, orientation='horizontal', pad=0.1)
cbar.ax.tick_params(labelsize=ticks_size)
cbar.set_label('Count', fontsize=colorbar_label_size)

plt.xticks(ticks=np.arange(len(cross_tab.columns)), labels=cross_tab.columns, rotation=70, fontsize=ticks_size, ha='center')
plt.yticks(ticks=np.arange(len(cross_tab.index)), labels=cross_tab.index, fontsize=ticks_size)

for (i, j), val in np.ndenumerate(cross_tab.values):
    ax.text(j, i, val, ha='center', va='center', color='white' if val > cross_tab.values.max()/2 else 'black', fontsize=cell_text_size)

plt.show()








