# This script processes and plots the retrieved data, which was gained from the other two files

import pandas as pd
import matplotlib.plotly as plt
import numpy as np
import seaborn as sns

# Import the retrieved data
reentry_df = pd.read_csv(r'C:\Users\[USER]\Desktop\ReentryData.csv')
object_df = pd.read_csv(r'C:\Users\[USER]\Desktop\SpaceObjects.csv')

# Create a column with an id number in object_df in order to join the reentry_df on this column
object_df['DiscosID'] = object_df['reentry_link'].str.strip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,:;()[]!@#$%^&*_-+=|\\/?`~ ').astype(int)

# Join the data on the id column
object_df = object_df.join(reentry_df.set_index('DiscosID'), on='DiscosID', how='left')
object_df.drop('Unnamed: 0', axis=1, inplace=True)

# Reentry means it's not orbiting, so filter out all the objects that have reentry data.
orbiting_df = object_df[object_df['epoch'].isna()]

orbiting_df.drop(['epoch', 'reentry_link'], axis=1, inplace=True) # Drop now useless columns
orbiting_df.describe()

# Look for the obj with the most mass (the ISS)
orbiting_df.loc[orbiting_df['mass'] == 450000]



# Plot creation
# Creating Box, Strip, and Histogram plots for 'mass' of the 21,165 tracked and in-orbit objects with known mass, which are found in the DiscosWeb Database.

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

sns.boxplot(data=all_orbiting_obj_df, x='mass',log_scale=True, ax=ax1,
            flierprops={'markersize': 5}, showfliers=False)

sns.stripplot(data=df, x="mass", ax=ax1, alpha=1, color="steelblue", size=3, jitter=0.01)


sns.histplot(data= all_orbiting_obj_df, x='mass', log_scale=True, bins=40, ax=ax2)



plt.xlabel('Mass (kg)')
fig.suptitle('Mass of Orbiting Objects')


ax1.xaxis.set_major_locator(LogLocator(base=10, numticks=10))
ax2.xaxis.set_major_locator(LogLocator(base=10, numticks=10))
ax1.set_xlim(left=0.01)

plt.tight_layout()

plt.subplots_adjust(hspace=0.01)





# Line Plot Creation
# Plotting Changes in Space Object Amount over Time (years). Dropping 2026 because it likely didn't take data from the whole year.
orbiting_df['firstEpoch'] = pd.to_datetime(orbiting_df['firstEpoch'])

lineplot_data = orbiting_df
lineplot_data = lineplot_data[lineplot_data['firstEpoch'].notna()]

lineplot_data['year'] = lineplot_data['firstEpoch'].dt.year.astype(int)
lineplot_data.reset_index(drop=True)

year_data = pd.DataFrame(lineplot_data['year'].value_counts())
year_data['years'] = year_data.index

year_data = year_data.reset_index(drop=True).sort_values(by='years')
year_data = year_data[year_data['years'] != 2026]


year_data
sns.lineplot(data=year_data, x='years', y='count')




# Calculations to try to estimate average volume per space object

# Find the volume of every orbiting object (v = m/density). Density is assumed to be 500 kg/m^3 (that of an average small satellite (not a certain estimate))

volume_df = orbiting_df.reset_index(drop=True)


# 866.22 kg avg mass per object
avgmass = np.mean(volume_df['mass'])

vol = avgmass / 500   # Dividing by avg density (500), both in kg, and m^3 remains

vol    # 1.73 m^3
# The (estimated) average volume of every object is 1.73 cubic meters


num_of_obj = (len(volume_df['mass']))

1.73 * num_of_obj

# 1.73 times the number of objects with mass in orbit gives 36,615 cubic meters of volume
# Therefore, an estimate for the total volume of all objects equals 36,615 m^3, or about 39 International Space Stations











