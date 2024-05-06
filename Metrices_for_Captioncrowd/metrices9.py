import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
        'Session Number': [],
        'Correct Identifications': [],
        'Missed Identifications': [],
        'False Negatives': [],
        'False Positives': []
    }

    for (user_name, session_number), group in df.groupby(['User Name', 'Session Number']):
        correct_idents = group[(group['Clicked Word'] != group['Exact Word']) &
                               (group['Exact Word'] != "Word not found")].shape[0]
        missed_idents = group[group['Exact Word'] == "Word not found"].shape[0]
        false_positives = group[(group['Clicked Word'] == group['Exact Word']) &
                                (group['Exact Word'] != "Word not found")].shape[0]
        total_errors = video_errors_dict.get(group['Video Name'].iloc[0], 0)
        false_negatives = total_errors - correct_idents

        results['User Name'].append(user_name)
        results['Session Number'].append(session_number)
        results['Correct Identifications'].append(correct_idents)
        results['Missed Identifications'].append(missed_idents)
        results['False Negatives'].append(false_negatives)
        results['False Positives'].append(false_positives)

    return pd.DataFrame(results)

# Calculate identifications and metrics
identifications = calculate_identifications(user_df)

# Convert 'User Name' to categorical with sorted order
user_df['User Name'] = pd.Categorical(user_df['User Name'], categories=user_df['User Name'].unique(), ordered=True)

# Create a summary DataFrame for box plot
metrics_summary = identifications.groupby(['User Name', 'Session Number'])[['Correct Identifications', 'Missed Identifications', 'False Negatives', 'False Positives']].sum()

# Melt the DataFrame to get it ready for Seaborn
melted_metrics_summary = metrics_summary.reset_index().melt(id_vars=['User Name', 'Session Number'], var_name='Metric', value_name='Count')
print(identifications)

# Create the box plot for the metrics
plt.figure(figsize=(10, 6))
sns.boxplot(data=melted_metrics_summary, x='Metric', y='Count', hue='Session Number')
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

# Extract unique session numbers
unique_sessions = identifications['Session Number'].unique()


# Sort 'User Name' lexically for consistent plotting
identifications['User Name'] = identifications['User Name'].astype(str).str.extract('(\d+)').astype(int)
identifications.sort_values('User Name', inplace=True)

# Loop through each session number and plot the bar graph
for session_number in unique_sessions:
    # Extract data for the current session number
    session_data = identifications[identifications['Session Number'] == session_number]
    
    # Extract data for Correct Identifications and False Positives
    correct_identifications_data = session_data.groupby('User Name')['Correct Identifications'].sum()
    false_positives_data = session_data.groupby('User Name')['False Positives'].sum()
    
    # Sort the data lexically by user name
    correct_identifications_data = correct_identifications_data.sort_index()
    false_positives_data = false_positives_data.sort_index()
    
    # Sort user names lexically
    sorted_user_names = correct_identifications_data.index.tolist()
    
    # Convert user names to the desired format (e.g., "User 1", "User 2", ...)
    formatted_user_names = ['User {}'.format(name) for name in sorted_user_names]

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    
    # Bar width
    bar_width = 0.35
    
    # Position of bars on x-axis
    r1 = range(len(correct_identifications_data))
    r2 = [x + bar_width for x in r1]
    
    # Plot bars for Correct Identifications
    plt.bar(r1, correct_identifications_data, color='saddlebrown', width=bar_width, edgecolor='grey', label='Correct Identifications')
    
    # Plot bars for False Positives
    plt.bar(r2, false_positives_data, color='darkkhaki', width=bar_width, edgecolor='grey', label='False Positives')
    
    # Add labels and title
    plt.xlabel('User Name', fontweight='bold')
    plt.ylabel('Count', fontweight='bold')
    plt.title(f'Correct Identifications and False Positives for Session {session_number}')
    plt.xticks([r + bar_width / 2 for r in range(len(correct_identifications_data))], formatted_user_names, rotation=45)
    plt.legend()
    
    # Show plot
    plt.tight_layout()
    plt.show()
