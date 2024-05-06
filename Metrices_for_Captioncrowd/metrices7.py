import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from natsort import natsorted
import matplotlib
matplotlib.use('TkAgg') 


# Load user interactions data
user_interactions_file_path = 'D:/python script for metrices/sorted_file.csv'  # Update with your actual path
user_df = pd.read_csv(user_interactions_file_path)

# Load total errors data
total_errors_file_path = 'D:/python script for metrices/totalerror.xlsx'  # Update with your actual path
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

# Create a summary DataFrame for box plot
metrics_summary = identifications.groupby('User Name')[['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']].sum()

# Melt the DataFrame to get it ready for Seaborn
melted_metrics_summary = metrics_summary.reset_index().melt(id_vars='User Name', var_name='Metric', value_name='Count')

# Create the box plot for the metrics
plt.figure(figsize=(10, 6))
sns.boxplot(data=melted_metrics_summary, x='Metric', y='Count')
plt.title('Box Plot of User Metrics')
plt.ylabel('Count')
plt.xlabel(' ')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Perform ANOVA for each metric
metrics = ['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']
anova_results = {}

for metric in metrics:
    # Prepare a list of series, each containing the metric values for each user
    data = [group[metric].values for _, group in identifications.groupby('User Name')]
    
    # Perform the ANOVA test
    F, p = stats.f_oneway(*data)
    
    # Store the results
    anova_results[metric] = {'F-statistic': F, 'p-value': p}

# Convert the results to a DataFrame for nicer display
anova_results_df = pd.DataFrame(anova_results).T
print("\nANOVA Results:\n", anova_results_df)

# Check normality for the metrics
normality_results = {}
for metric in metrics:
    stat, p = stats.shapiro(identifications[metric])
    normality_results[metric] = {'Shapiro-Wilk Statistic': stat, 'p-value': p}

# Convert the results to a DataFrame for nicer display
normality_results_df = pd.DataFrame(normality_results).T
print("\nNormality Check Results:\n", normality_results_df)






