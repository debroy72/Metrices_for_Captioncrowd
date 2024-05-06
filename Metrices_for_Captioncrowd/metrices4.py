import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from natsort import natsorted

# Load user interactions data
user_interactions_file_path = 'D:/python script for metrices/sorted_file.csv'
user_df = pd.read_csv(user_interactions_file_path)

# Load total errors data
total_errors_file_path = 'D:/python script for metrices/totalerror.xlsx'
video_errors_df = pd.read_excel(total_errors_file_path)

# Strip trailing spaces from column names
video_errors_df.columns = video_errors_df.columns.str.strip()

# Create a dictionary to map video names to their total errors
video_errors_dict = dict(zip(video_errors_df['Video Name'], video_errors_df['Total number of error']))

# Function to calculate correct, missed identifications, false negatives, and false positives
def calculate_identifications(df):
    results = {
        'User Name': [],
        'Video Name': [],
        'Correct Identifications': [],
        'Missed Identifications': [],
        'False Negatives': [],
        'False Positives': []
    }

    for (user_name, video_name), group in df.groupby(['User Name', 'Video Name']):
        correct_idents = group[(group['Clicked Word'] != group['Exact Word']) &
                               (group['Exact Word'] != "Word not found")].shape[0]
        missed_idents = group[group['Exact Word'] == "Word not found"].shape[0]
        false_positives = group[(group['Clicked Word'] == group['Exact Word']) &
                                (group['Exact Word'] != "Word not found")].shape[0]
        total_errors = video_errors_dict.get(video_name, 0)
        false_negatives = total_errors - correct_idents

        results['User Name'].append(user_name)
        results['Video Name'].append(video_name)
        results['Correct Identifications'].append(correct_idents)
        results['Missed Identifications'].append(missed_idents)
        results['False Negatives'].append(false_negatives)
        results['False Positives'].append(false_positives)

    return pd.DataFrame(results)

# Calculate identifications and metrics
identifications = calculate_identifications(user_df)

# Sort 'User Name' lexically for consistent plotting
identifications['User Name'] = identifications['User Name'].astype(str).str.extract('(\d+)').astype(int)
identifications.sort_values('User Name', inplace=True)

# Reset the 'User Name' to its original form if needed for presentation
identifications['User Name'] = 'User ' + identifications['User Name'].astype(str)

identifications['Accuracy Count'] = identifications['Correct Identifications']
total_accuracy_per_user = identifications.groupby('User Name')['Accuracy Count'].sum()

# Displaying the results
print("Identifications and Accuracy Counts:")
print(identifications)
print("\nTotal Accuracy Count per User:")
print(total_accuracy_per_user)

# Plotting Total Accuracy Count for Each User with lexical sorting
plt.figure(figsize=(10, 6))
sorted_user_names = natsorted(total_accuracy_per_user.index)
sns.barplot(x=sorted_user_names, y=total_accuracy_per_user.loc[sorted_user_names].values)
plt.title('Total Accuracy Count per User')
plt.ylabel('Accuracy Count')
plt.xlabel('User Name')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Preparing data for stacked bar chart including False Positives
stacked_data = identifications.groupby('User Name').sum()[['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']]

# Sorting the index of stacked_data lexically based on the numeric part of the 'User Name'
stacked_data = stacked_data.reindex(index=natsorted(stacked_data.index))

# Plotting the sorted stacked bar chart
stacked_data.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Metrics per User')
plt.ylabel('Count')
plt.xlabel('User Name')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Assuming identifications DataFrame is processed as per your previous code

# Group data by 'User Name' and calculate the sum of all metrics for each user
total_counts_per_user = identifications.groupby('User Name')[['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']].sum().sum(axis=1)

# Plotting the aggregated total for each user
plt.figure(figsize=(14, 8))
sns.barplot(x=total_counts_per_user.index, y=total_counts_per_user.values)
plt.title('Aggregated Total Count per User')
plt.ylabel('Total Count')
plt.xlabel('User Name')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Plotting Box and Whisker plot with additional labelings
numeric_cols = ['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']
melted_data = identifications.melt(id_vars=['User Name'], value_vars=numeric_cols, var_name='Metric', value_name='Count')
melted_data['Count'] = pd.to_numeric(melted_data['Count'], errors='coerce')

plt.figure(figsize=(14, 8))
sns.boxplot(x='Metric', y='Count', data=melted_data, palette="Set2")
plt.title('Distribution of User Metrics', fontsize=16)
plt.xlabel('Metric', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)

medians = melted_data.groupby(['Metric'])['Count'].median()
for idx, median in medians.iteritems():
    plt.text(x=numeric_cols.index(idx), y=median + 0.5, s=f'{median:.2f}',
             ha='center', va='bottom', fontsize=9, color='black')

plt.tight_layout()
plt.show()
