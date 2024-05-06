import pandas as pd
from scipy import stats

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

# Perform Mann-Whitney U test for each metric between pairs of users
mann_whitney_results = {}

metrics = ['Correct Identifications', 'Missed Identifications', 'False Positives']

for metric in metrics:
    # Prepare a list of series, each containing the metric values for each user
    data_mw = [group[metric].values for _, group in identifications.groupby('User Name')]
    
    # Perform Mann-Whitney U test for each pair of users
    for i in range(len(data_mw)):
        for j in range(i+1, len(data_mw)):
            user1 = identifications['User Name'].unique()[i]
            user2 = identifications['User Name'].unique()[j]
            U_statistic, p_value = stats.mannwhitneyu(data_mw[i], data_mw[j], alternative='two-sided')
            comparison_key = f'{user1} vs {user2}'
            if metric not in mann_whitney_results:
                mann_whitney_results[metric] = {'U-statistic': [], 'p-value': []}
            mann_whitney_results[metric]['U-statistic'].append(U_statistic)
            mann_whitney_results[metric]['p-value'].append(p_value)

# Calculate the average U-statistic and p-value for each metric
average_mw_results = {}
for metric, results in mann_whitney_results.items():
    average_U = sum(results['U-statistic']) / len(results['U-statistic'])
    average_p = sum(results['p-value']) / len(results['p-value'])
    average_mw_results[metric] = {'Average U-statistic': average_U, 'Average p-value': average_p}

# Convert the results to a DataFrame for nicer display
average_mw_results_df = pd.DataFrame(average_mw_results).T
print("\nAverage Mann-Whitney U Test Results:")
print(average_mw_results_df)
