"""
import pandas as pd

# Load the spreadsheet
file_path = '/Users/jadew/Desktop/diabetes/Jade0816.xlsx'
data = pd.read_excel(file_path)

# Rename all columns (ensure this list has exactly 48 names as per your dataset)
data.columns = [
    'Article_ID', 'Title', 'Pub_Date', 'Year', 'Source_Specific', 'Source', 
    'Author', 'New_Study', 'Reporting_Frame', 'Mentioned_T1', 'Mentioned_T2', 
    'Mentioned_LADA', 'Mentioned_Unspecified', 'Behavioral_0', 'Societal_0', 
    'Medical_0', 'Prominent_Frame_0', 'Behavioral_1', 'Societal_1', 'Medical_1', 
    'Prominent_Frame_1', 'Behavioral_2', 'Societal_2', 'Medical_2', 'Prominent_Frame_2', 
    'Behavioral_3', 'Societal_3', 'Medical_3', 'Prominent_Frame_3', 'Behavioral_4', 
    'Societal_4', 'Medical_4', 'Prominent_Frame_4', 'Supplies_Affordability', 
    'Insulin_Pricing', 'Insulin_Rationing', 'Hospitalization', 'Death', 
    'New_Meds', 'Meds_Name', 'CGM_Mentioned', 'AID_Mentioned', 'Obesity_Weight', 
    'Prediabetes', 'Mentioned_Both', 'Article_Contains', 'Key_Excerpt', 'Notes'
]

# Ensure 'Reporting_Frame' includes all categories (1, 2, 3, 4)
data['Reporting_Frame'] = pd.Categorical(
    data['Reporting_Frame'],
    categories=[1, 2, 3, 4],
    ordered=True
)

# Create a new column 'Source_Grouped' that groups CNN and CNN Wire together
data['Source_Grouped'] = data['Source'].replace({
    'CNN': 'CNN/CNN Wire',
    'CNN Wire': 'CNN/CNN Wire',
    'NYT': 'NYT'
})

# Group by 'Source_Grouped' and 'Reporting_Frame'
frame_by_source = data.groupby(['Source_Grouped', 'Reporting_Frame']).size().unstack().fillna(0)

# Optionally, ensure the columns are ordered correctly
frame_by_source = frame_by_source[[1, 2, 3, 4]]

# Display the result
#print(frame_by_source)
# Append the result to an HTML file
#with open('diabetes_results.html', 'a') as f:
    #f.write(frame_by_source.to_html())
# Convert 'Year' to string and filter out non-numeric values
data = data[data['Year'].astype(str).apply(lambda x: x.isnumeric())]

# Now safely convert 'Year' to integers
data['Year'] = data['Year'].astype(int)
# Group by 'Year' and 'Reporting_Frame'
frame_by_year = data.groupby(['Year', 'Reporting_Frame']).size().unstack().fillna(0)

# Optionally, ensure the columns are ordered correctly
frame_by_year = frame_by_year[[1, 2, 3, 4]]

# Display the result
#print(frame_by_year)

# Group by 'Year', 'Source_Grouped', and 'Reporting_Frame', then unstack 'Reporting_Frame'
frame_by_year_and_source = data.groupby(['Year', 'Source_Grouped', 'Reporting_Frame']).size().unstack().fillna(0)

# Optionally, ensure the columns for 'Reporting_Frame' are ordered correctly
frame_by_year_and_source = frame_by_year_and_source[[1, 2, 3, 4]]

# Print the result
#print("Reporting Frame sorted by Year and broken down by Source Grouped:")
#with open('diabetes_results.html', 'a') as f:
    #f.write(frame_by_year_and_source.to_html())

import pandas as pd
import matplotlib.pyplot as plt

# Load the spreadsheet
file_path = '/Users/jadew/Desktop/diabetes/Jade0816.xlsx'
data = pd.read_excel(file_path)

# Rename all columns
data.columns = [
    'Article_ID', 'Title', 'Pub_Date', 'Year', 'Source_Specific', 'Source', 
    'Author', 'New_Study', 'Reporting_Frame', 'Mentioned_T1', 'Mentioned_T2', 
    'Mentioned_LADA', 'Mentioned_Unspecified', 'Behavioral_0', 'Societal_0', 
    'Medical_0', 'Prominent_Frame_0', 'Behavioral_1', 'Societal_1', 'Medical_1', 
    'Prominent_Frame_1', 'Behavioral_2', 'Societal_2', 'Medical_2', 'Prominent_Frame_2', 
    'Behavioral_3', 'Societal_3', 'Medical_3', 'Prominent_Frame_3', 'Behavioral_4', 
    'Societal_4', 'Medical_4', 'Prominent_Frame_4', 'Supplies_Affordability', 
    'Insulin_Pricing', 'Insulin_Rationing', 'Hospitalization', 'Death', 
    'New_Meds', 'Meds_Name', 'CGM_Mentioned', 'AID_Mentioned', 'Obesity_Weight', 
    'Prediabetes', 'Mentioned_Both', 'Article_Contains', 'Key_Excerpt', 'Notes'
]

# Convert 'Mentioned_T1' to numeric, setting errors='coerce' to treat non-numeric values as NaN
data['Mentioned_T1'] = pd.to_numeric(data['Mentioned_T1'], errors='coerce')
data['Mentioned_T2'] = pd.to_numeric(data['Mentioned_T2'], errors='coerce')

# Now calculate the sum
total_type1 = data['Mentioned_T1'].sum()
total_type2 = data['Mentioned_T2'].sum()

# Calculate how many of those articles also mention obesity/weight
type1_with_obesity = data[(data['Mentioned_T1'] == 1) & (data['Obesity_Weight'] == 1)].shape[0]
type2_with_obesity = data[(data['Mentioned_T2'] == 1) & (data['Obesity_Weight'] == 1)].shape[0]

# Calculate the proportions
type1_obesity_proportion = type1_with_obesity / total_type1 if total_type1 != 0 else 0
type2_obesity_proportion = type2_with_obesity / total_type2 if total_type2 != 0 else 0

# Prepare data for plotting
labels = ['Type 1 Diabetes', 'Type 2 Diabetes']
proportions = [type1_obesity_proportion, type2_obesity_proportion]

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(labels, proportions, color=['blue', 'green'])

# Add titles and labels
plt.title('Proportion of Articles Mentioning Obesity/Weight\nin Type 1 and Type 2 Diabetes Coverage', fontsize=16)
plt.xlabel('Type of Diabetes', fontsize=14)
plt.ylabel('Proportion of Articles Mentioning Obesity/Weight', fontsize=14)

# Show the values on top of the bars
for i, v in enumerate(proportions):
    plt.text(i, v + 0.01, f"{v:.2%}", ha='center', fontsize=12)

# Display the plot
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Save the plot as an image
plt.savefig('/Users/jadew/Desktop/diabetes/diabetes_plot.png')

# Write the image into an HTML file
with open('/Users/jadew/Desktop/diabetes/diabetes_results.html', 'a') as f:
    f.write('<img src="diabetes_plot.png" alt="Diabetes Data Plot">')
"""
import pandas as pd
import matplotlib.pyplot as plt

# Load the spreadsheet
file_path = '/Users/jadew/Desktop/diabetes/Jade0816.xlsx'
data = pd.read_excel(file_path)

# Rename all columns
data.columns = [
    'Article_ID', 'Title', 'Pub_Date', 'Year', 'Source_Specific', 'Source', 
    'Author', 'New_Study', 'Reporting_Frame', 'Mentioned_T1', 'Mentioned_T2', 
    'Mentioned_LADA', 'Mentioned_Unspecified', 'Behavioral_0', 'Societal_0', 
    'Medical_0', 'Prominent_Frame_0', 'Behavioral_1', 'Societal_1', 'Medical_1', 
    'Prominent_Frame_1', 'Behavioral_2', 'Societal_2', 'Medical_2', 'Prominent_Frame_2', 
    'Behavioral_3', 'Societal_3', 'Medical_3', 'Prominent_Frame_3', 'Behavioral_4', 
    'Societal_4', 'Medical_4', 'Prominent_Frame_4', 'Supplies_Affordability', 
    'Insulin_Pricing', 'Insulin_Rationing', 'Hospitalization', 'Death', 
    'New_Meds', 'Meds_Name', 'CGM_Mentioned', 'AID_Mentioned', 'Obesity_Weight', 
    'Prediabetes', 'Mentioned_Both', 'Article_Contains', 'Key_Excerpt', 'Notes'
]

# Filter data to include only articles that mention Type 2 diabetes and obesity/weight
filtered_data = data[(data['Mentioned_T2'] == 1) & (data['Obesity_Weight'] == 1)]

# Group by the most prominent frame (Prominent_Frame_2) and count the occurrences
frame_breakdown = filtered_data['Prominent_Frame_2'].value_counts().sort_index()

# Mapping frame numbers to labels
frame_labels = {1: 'Behavioral', 2: 'Societal', 3: 'Medical', 4: 'Indeterminate', 99: 'No frame used'}  # Adjust labels as needed
frame_breakdown.index = frame_breakdown.index.map(frame_labels)

# Plot the results
plt.figure(figsize=(12, 8))
frame_breakdown.plot(kind='bar', color='skyblue')

# Add titles and labels
plt.title('Breakdown of Most Prominent Frames in Type 2 Diabetes Articles Mentioning Obesity/Weight', fontsize=16)
plt.xlabel('Most Prominent Frame', fontsize=14)
plt.ylabel('Number of Articles', fontsize=14)
plt.xticks(rotation=45)

# Show the plot
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
