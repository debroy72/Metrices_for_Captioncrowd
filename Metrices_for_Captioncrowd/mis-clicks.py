import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_1samp

# Load the user interactions data
user_interactions_file_path = 'D:/python script for metrices/user_interactions.csv.csv'
print("Loading data...")
user_df = pd.read_csv(user_interactions_file_path)
print("Data loaded successfully.")

# Create a new column for mis-clicks
user_df['Mis-click'] = (user_df['Clicked Word'] != user_df['Exact Word']).astype(int)
print("Mis-click column created.")

# Group by various attributes and calculate mis-click frequency
mis_clicks_by_user = user_df.groupby('User Name')['Mis-click'].mean()
mis_clicks_by_video = user_df.groupby('Video Name')['Mis-click'].mean()
mis_clicks_by_subtitle = user_df.groupby('Subtitle Number')['Mis-click'].mean()
print("Mis-click frequency calculated.")

# Statistical Analysis
t_stat, p_value = ttest_1samp(user_df['Mis-click'], 0.5)
print(f"T-statistic: {t_stat}, P-value: {p_value}")

# Visual Representation
# Heatmap for mis-clicks by user
plt.figure(figsize=(12, 6))
sns.barplot(x=mis_clicks_by_user.index, y=mis_clicks_by_user.values)
plt.title('Mis-click Rate by User')
plt.xlabel('User Name')
plt.ylabel('Mis-click Rate')
plt.xticks(rotation=45)
plt.show()

# Bar chart for mis-click frequency by subtitle
plt.figure(figsize=(14, 6))
mis_clicks_by_subtitle.plot(kind='bar', color='skyblue')
plt.title('Mis-click Frequency by Subtitle Number')
plt.xlabel('Subtitle Number')
plt.ylabel('Mis-click Rate')
plt.show()

print("Script execution completed.")
