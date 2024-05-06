import pandas as pd
import matplotlib.pyplot as plt

# Load the user interactions data
user_interactions_file_path = 'D:/python script for metrices/user_interactions.csv'
user_df = pd.read_csv(user_interactions_file_path)

# Convert 'Timestamp' from MM:SS to seconds for uniformity
def timestamp_to_seconds(timestamp):
    m, s = map(int, timestamp.split(':'))
    return m * 60 + s

user_df['Timestamp Seconds'] = user_df['Timestamp'].apply(timestamp_to_seconds)

# Analyze click frequency per video
clicks_per_video = user_df.groupby('Video Name').size().reset_index(name='Clicks')

# Analyze click frequency per session
clicks_per_session = user_df.groupby('Session Number').size().reset_index(name='Clicks')

# Analyze click frequency per user
clicks_per_user = user_df.groupby('User Name').size().reset_index(name='Clicks')

# Plotting for insights
plt.figure(figsize=(14, 6))
clicks_per_video.sort_values(by='Clicks', ascending=False).plot.bar(x='Video Name', y='Clicks', legend=False)
plt.title('Click Frequency Per Video')
plt.xlabel('Video Name')
plt.ylabel('Number of Clicks')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 6))
clicks_per_session.sort_values(by='Clicks', ascending=False).plot.bar(x='Session Number', y='Clicks', legend=False)
plt.title('Click Frequency Per Session')
plt.xlabel('Session Number')
plt.ylabel('Number of Clicks')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 6))
clicks_per_user.sort_values(by='Clicks', ascending=False).plot.bar(x='User Name', y='Clicks', legend=False)
plt.title('Click Frequency Per User')
plt.xlabel('User Name')
plt.ylabel('Number of Clicks')
plt.tight_layout()
plt.show()

# Determining patterns
# You may use statistical measures like mean, median, or standard deviation to find patterns.
# For example, to see if certain sessions have unusually high or low click counts:
average_clicks_per_session = clicks_per_session['Clicks'].mean()
std_clicks_per_session = clicks_per_session['Clicks'].std()

# Flag sessions with high engagement
high_engagement_sessions = clicks_per_session[clicks_per_session['Clicks'] > (average_clicks_per_session + std_clicks_per_session)]

print("High Engagement Sessions:")
print(high_engagement_sessions)

# Similarly, you can perform this analysis for users and videos.
