import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading dataset...")
df = pd.read_csv('All_Diets.csv')
print("Dataset loaded successfully!\n")

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
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.xlabel('Diet Type')
plt.ylabel('Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('avg_protein_bar_chart.png')
plt.show()

plt.figure(figsize=(10, 5))
sns.scatterplot(data=top_protein, x='Carbs(g)', y='Protein(g)', hue='Diet_type')
plt.title('Top 5 Protein-Rich Recipes (Protein vs Carbs)')
plt.xlabel('Carbs (g)')
plt.ylabel('Protein (g)')
plt.legend(title='Diet Type')
plt.tight_layout()
plt.savefig('protein_scatter_plot.png')
plt.show()

print("\nVisualizations saved as:")
print(" - avg_protein_bar_chart.png")
print(" - protein_scatter_plot.png")

print("\n Task 1 completed successfully!")

import numpy as np

print("\nStarting Task 2 (NumPy-based analysis)...")

protein = df['Protein(g)'].to_numpy()
carbs = df['Carbs(g)'].to_numpy()
fat = df['Fat(g)'].to_numpy()

print("\nNumpy statistical results:")
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
plt.show()

print("\nTask 2 completed successfully!")
print("\nVisualizations saved as:")
print(" - total_macros_histogram.png")
