import pandas as pd

# Input and output file paths
input_file = "202503-citibike-tripdata.csv"
output_file = "citibike_stations.csv"

# Relevant columns
cols = ['start_station_id', 'start_station_name', 'start_lat', 'start_lng']

# Read CSV with start_station_id as string
df = pd.read_csv(input_file, usecols=cols, dtype={'start_station_id': str})

# Drop rows with missing data
df = df.dropna(subset=['start_station_name', 'start_lat', 'start_lng'])

# Helper function to get most frequent value
def most_common(series):
    return series.value_counts().idxmax()

# Group by station name
grouped = df.groupby('start_station_name').agg({
    'start_station_id': most_common,
    'start_lat': most_common,
    'start_lng': most_common
}).reset_index()

# Reorder columns
grouped = grouped[['start_station_id', 'start_station_name', 'start_lat', 'start_lng']]

# Save to CSV
grouped.to_csv(output_file, index=False)

print(f"Saved {len(grouped)} unique start stations (by name) to {output_file}.")
