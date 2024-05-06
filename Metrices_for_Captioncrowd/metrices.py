import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load user interactions data
user_interactions_file_path = 'D:/python script for metrices/anonymous_user_interactions.csv'
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
        'False Positives': []  # Adding false positives
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

# Calculate correct, missed identifications, false negatives, and false positives
identifications = calculate_identifications(user_df)

# Calculating the percentage of correct identifications to total errors
identifications['Identification to Error Percentage'] = identifications.apply(
    lambda row: (row['Correct Identifications'] / video_errors_dict.get(row['Video Name'], 0)) * 100 if video_errors_dict.get(row['Video Name'], 0) else 0, axis=1
)

# Calculate the average accuracy percentage for each user
average_accuracy_per_user = identifications.groupby('User Name')['Identification to Error Percentage'].mean()

# Display the final results
print("Identifications and Error Percentages:")
print(identifications)

# Display the average accuracy percentages for each user
print("\nAverage Accuracy Percentage per User:")
print(average_accuracy_per_user)

# Plotting Average Accuracy for Each User
plt.figure(figsize=(10, 6))
sns.barplot(x=average_accuracy_per_user.index, y=average_accuracy_per_user.values)
plt.title('Average Accuracy Rate per User')
plt.ylabel('Accuracy Rate (%)')
plt.xlabel('User Name')
plt.show()

# Preparing data for stacked bar chart including False Positives
stacked_data = identifications.groupby('User Name').sum()[['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']]
stacked_data.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Metrics per User')
plt.ylabel('Count')
plt.xlabel('User Name')
plt.show()


# Selecting only the numeric columns for the boxplot (excluding 'User Name' and 'Video Name')
numeric_cols = ['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']
melted_data = identifications.melt(id_vars=['User Name'], value_vars=numeric_cols, var_name='Metric', value_name='Count')

# Ensure that 'Count' is numeric after melting
melted_data['Count'] = pd.to_numeric(melted_data['Count'], errors='coerce')

# Plotting Box and Whisker plot with additional labelings
plt.figure(figsize=(14, 8))  # Specify the figure size
sns.boxplot(x='Metric', y='Count', data=melted_data, palette="Set2")  # Choose a color palette for the plot
plt.title('Distribution of User Metrics', fontsize=16)  # Set the title of the plot
plt.xlabel('Metric', fontsize=14)  # Set the x-axis label
plt.ylabel('Count', fontsize=14)  # Set the y-axis label
plt.xticks(rotation=45, fontsize=12)  # Rotate x-axis labels and set font size
plt.yticks(fontsize=12)  # Set y-axis labels font size
plt.grid(True)  # Add grid for better readability

# Adding median value labels on the plot
medians = melted_data.groupby(['Metric'])['Count'].median()
for idx, median in medians.iteritems():
    plt.text(x=idx, y=median + 0.5, s=f'{median:.2f}', 
             ha='center', va='bottom', fontsize=9, color='black')

plt.tight_layout()  # Adjust layout to prevent clipping of ylabel
plt.show()