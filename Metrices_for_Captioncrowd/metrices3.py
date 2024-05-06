import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load user interactions data from CSV
user_interactions_file_path = 'D:/python script for metrices/anonymous_user_interactions.csv'
user_df = pd.read_csv(user_interactions_file_path)

# Load total errors data from Excel
total_errors_file_path = 'D:/python script for metrices/totalerror.xlsx'
video_errors_df = pd.read_excel(total_errors_file_path)

# Strip trailing spaces from column names in the Excel data
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

# Calculating identification metrics
identifications = calculate_identifications(user_df)

# Adjusted section for mean calculation
numeric_columns = ['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']
mean_metrics_per_user = identifications.groupby('User Name')[numeric_columns].mean().reset_index()

# Melting the DataFrame for seaborn compatibility
melted_data = mean_metrics_per_user.melt(id_vars=['User Name'], value_vars=numeric_columns, var_name='Metric', value_name='Average Count')

# Plotting the box and whisker plot
plt.figure(figsize=(14, 8))
sns.boxplot(x='Metric', y='Average Count', data=melted_data, palette="Set2")
plt.title('Average Distribution of Metrics per User', fontsize=16)
plt.xlabel('Metric', fontsize=14)
plt.ylabel('Average Count', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
