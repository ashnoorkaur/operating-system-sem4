import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import time

load_dotenv()


print("Loading dataset...")
try:
    df = pd.read_csv('All_Diets.csv')
    print("Dataset loaded successfully!\n")
except FileNotFoundError:
    print("ERROR: 'All_Diets.csv' not found. Make sure the file exists in the same directory.")
    exit()

print(df.head())

df.fillna(df.mean(numeric_only=True), inplace=True)

print("\nCalculating average macronutrients...")
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
print(avg_macros)

print("\nFinding top 5 protein-rich recipes per diet type...")
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']])

print("\nAdding ratio metrics...")
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

df.to_csv('All_Diets_cleaned.csv', index=False)
print("\nCleaned dataset saved as 'All_Diets_cleaned.csv'")

print("\nGenerating visualizations...")

plt.figure(figsize=(10, 5))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'], palette='coolwarm')
plt.title('Average Protein by Diet Type')
plt.xlabel('Diet Type')
plt.ylabel('Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('avg_protein_bar_chart.png')
plt.close()

plt.figure(figsize=(10, 5))
sns.scatterplot(data=top_protein, x='Carbs(g)', y='Protein(g)', hue='Diet_type', palette='viridis', s=80)
plt.title('Top 5 Protein-Rich Recipes (Protein vs Carbs)')
plt.xlabel('Carbs (g)')
plt.ylabel('Protein (g)')
plt.legend(title='Diet Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('protein_scatter_plot.png')
plt.close()

print("\nVisualizations saved:")
print(" - avg_protein_bar_chart.png")
print(" - protein_scatter_plot.png")
print("\nTask 1 completed successfully!")

print("\nStarting Task 2 (NumPy-based analysis)...")

protein = df['Protein(g)'].to_numpy()
carbs = df['Carbs(g)'].to_numpy()
fat = df['Fat(g)'].to_numpy()

print("\nNumPy Statistical Results:")
print(f"Mean Protein: {np.mean(protein):.2f}")
print(f"Mean Carbs: {np.mean(carbs):.2f}")
print(f"Mean Fat: {np.mean(fat):.2f}")
print(f"Max Protein: {np.max(protein):.2f}")
print(f"Min Protein: {np.min(protein):.2f}")

total_macros = np.column_stack((protein, carbs, fat))
total_sum = np.sum(total_macros, axis=1)

df['Total_macros'] = total_sum
df.to_csv('All_Diets_NP_Results.csv', index=False)
print("\nUpdated dataset saved as 'All_Diets_NP_Results.csv'")

plt.figure(figsize=(10, 5))
plt.hist(total_sum, bins=20, edgecolor='black')
plt.title('Distribution of Total Macronutrients')
plt.xlabel('Total Macronutrient Content')
plt.ylabel('Number of Recipes')
plt.tight_layout()
plt.savefig('total_macros_histogram.png')
plt.close()

print("\nVisualizations saved:")
print(" - total_macros_histogram.png")
print("\nTask 2 completed successfully!")

print("\nStarting Task 3: Uploading files to Azure Blob Storage...\n")

CONTAINER_NAME = "diets-data"
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not connection_string:
    print("Azure connection string not found in environment variables.")
    print("Set it using:")
    print("   export AZURE_STORAGE_CONNECTION_STRING='your_connection_string_here'")
    exit()

try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    files_to_upload = [
        "All_Diets_cleaned.csv",
        "All_Diets_NP_Results.csv",
        "avg_protein_bar_chart.png",
        "protein_scatter_plot.png",
        "total_macros_histogram.png"
    ]

    for file_name in files_to_upload:
        if os.path.exists(file_name):
            print(f"Uploading {file_name} ...")
            with open(file_name, "rb") as data:
                container_client.upload_blob(name=file_name, data=data, overwrite=True)
            print(f"Uploaded: {file_name}")
            time.sleep(1)
        else:
            print(f"Skipped: {file_name} not found locally.")

    print("\nAll available files uploaded successfully to Azure Blob Storage!")
    print(f"Container name: {CONTAINER_NAME}")

except Exception as e:
    print("Error during Azure upload:", e)

print("\nAll Tasks (1, 2, and 3) executed successfully!")
