import pandas as pd
import matplotlib.pyplot as plt

# Load the user interactions data
user_interactions_file_path = 'D:/python script for metrices/user_interactions.csv'
user_df = pd.read_csv(user_interactions_file_path)

# Function to convert MM:SS to seconds
def timestamp_to_seconds(timestamp):
    m, s = map(int, timestamp.split(':'))
    return m * 60 + s

# Display timestamps before conversion
print("Timestamps before conversion to seconds:")
print(user_df['Timestamp'].head())

# Convert 'Timestamp' to seconds for each entry
user_df['Timestamp Seconds'] = user_df['Timestamp'].apply(timestamp_to_seconds)

# Display timestamps after conversion
print("\nTimestamps after conversion to seconds:")
print(user_df['Timestamp Seconds'].head())

# Define interval length in seconds (e.g., 60 for one-minute intervals)
interval_length = 10

# Assign each click to an interval
user_df['Interval'] = user_df['Timestamp Seconds'] // interval_length

# Group by 'Video Name' and 'Interval' and count clicks per interval
interval_click_counts = user_df.groupby(['Video Name', 'Interval']).size().reset_index(name='Clicks')

# Plot the click distribution for each video
for video_name, group in interval_click_counts.groupby('Video Name'):
    plt.figure(figsize=(14, 6))
    plt.plot(group['Interval'] * interval_length, group['Clicks'], marker='o', linestyle='-')
    plt.title(f'Click Distribution Over Time for {video_name}')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Number of Clicks')
    plt.grid(True)
    plt.show()
