import pandas as pd

# Load the dataset
df = pd.read_csv('waste_datset_final.csv')

# Group by region and calculate total wet and dry waste weight
region_waste = df.groupby('region_id').agg({
    'wet_waste': 'sum',
    'dry_waste': 'sum'
}).reset_index()

# Rank the regions based on wet waste weight
region_waste['wet_rank'] = region_waste['wet_waste'].rank(ascending=False)

# Rank the regions based on dry waste weight
region_waste['dry_rank'] = region_waste['dry_waste'].rank(ascending=False)

# Sort by rank in descending order
region_waste_sorted_wet = region_waste.sort_values(by='wet_rank', ascending=True)
region_waste_sorted_dry = region_waste.sort_values(by='dry_rank', ascending=True)

# Display the result
print("Ranking based on Wet Waste:")
print(region_waste_sorted_wet[['region_id', 'wet_waste', 'wet_rank']])

print("\nRanking based on Dry Waste:")
print(region_waste_sorted_dry[['region_id', 'dry_waste', 'dry_rank']])
