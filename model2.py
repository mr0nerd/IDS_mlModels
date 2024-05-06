import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix

# Generate dummy dataset
truck_id_range = np.arange(1100, 1201)
region_id_range = np.arange(1, 101)
day_no_range = np.arange(1, 91)

truck_ids = np.tile(truck_id_range, len(region_id_range) * len(day_no_range))
region_ids = np.tile(np.repeat(region_id_range, len(day_no_range)), len(truck_id_range))
day_nos = np.repeat(np.tile(day_no_range, len(region_id_range)), len(truck_id_range))

wet_waste = np.random.uniform(500, 3000, size=len(truck_ids))
dry_waste = np.random.uniform(500, 3000, size=len(truck_ids))

df = pd.DataFrame({
    'truck_id': truck_ids,
    'day_no': day_nos,
    'region_id': region_ids,
    'wet_waste': wet_waste,
    'dry_waste': dry_waste
})

# Calculate random distances between regions
np.random.seed(42)
region_coords = np.random.rand(len(region_id_range), 2)
distance_matrix = distance_matrix(region_coords, region_coords)

max_distance = np.max(distance_matrix)
distance_matrix_normalized = distance_matrix / max_distance

distance_df = pd.DataFrame(distance_matrix_normalized, index=region_id_range, columns=region_id_range)

# Print column names for debugging
print("Columns in df:", df.columns)
print("Columns in distance_df:", distance_df.columns)

# Concatenate distance columns to the main DataFrame
df = df.join(distance_df.add_prefix('distance_to_region_'), on='region_id')

df = df.head(1000)

# Save the dataset
df.to_csv('transactions_2019_sequential_1000_with_distances.csv', index=False)

# Load the dataset
df = pd.read_csv('transactions_2019_sequential_1000_with_distances.csv')

# Group by region and calculate mean wet and dry waste production
region_waste = df.groupby('region_id').agg({
    'wet_waste': 'mean',
    'dry_waste': 'mean'
}).reset_index()

# Find regions with highest wet waste production
top_wet_regions = region_waste.nlargest(5, 'wet_waste')['region_id']

# Find regions with highest dry waste production
top_dry_regions = region_waste.nlargest(5, 'dry_waste')['region_id']

# Function to find nearest region to a potential plant location
def find_nearest_region(plant_location, target_regions):
    min_distance = float('inf')
    nearest_region = None
    for region in target_regions:
        distance = df.loc[df['region_id'] == plant_location, f'distance_to_region_{region}']
        non_zero_distances = distance[distance != 0]  # Exclude zero distances
        if not non_zero_distances.empty:
            current_min_distance = non_zero_distances.min()
            if current_min_distance < min_distance:
                min_distance = current_min_distance
                nearest_region = region
    # Check if all distances are zero
    if min_distance == float('inf'):
        min_distance = 0
    return nearest_region, min_distance

# Find nearest regions to potential manure/biodegradable plant locations
manure_plant_locations = top_wet_regions
biodegradable_plant_locations = top_wet_regions
recycling_plant_locations = top_dry_regions

# Output potential plant locations along with nearest regions and distances
print("Potential Manure Plant Locations:")
for location in manure_plant_locations:
    nearest_region, min_distance = find_nearest_region(location, top_wet_regions)
    print(f"Location: {location}, Nearest Region with High Wet Waste Production: {nearest_region}, Distance: {min_distance}")

print("\nPotential Biodegradable Plant Locations:")
for location in biodegradable_plant_locations:
    nearest_region, min_distance = find_nearest_region(location, top_wet_regions)
    print(f"Location: {location}, Nearest Region with High Wet Waste Production: {nearest_region}, Distance: {min_distance}")

print("\nPotential Recycling Plant Locations:")
for location in recycling_plant_locations:
    nearest_region, min_distance = find_nearest_region(location, top_dry_regions)
    print(f"Location: {location}, Nearest Region with High Dry Waste Production: {nearest_region}, Distance: {min_distance}")
