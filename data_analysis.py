import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('All_Diets.csv')
print("Dataset loaded successfully!\n")

# Show first few rows
print(df.head())

# Clean missing values (replace with mean)
df.fillna(df.mean(numeric_only=True), inplace=True)

# Calculate average macronutrient content for each diet type
print("\nCalculating average macronutrients...")
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
print(avg_macros)

# Find the top 5 protein-rich recipes for each diet type
print("\nFinding top 5 protein-rich recipes per diet type...")
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
print(top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']])

# Add new metrics
print("\nAdding ratio metrics...")
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

# Save cleaned dataset
df.to_csv('All_Diets_cleaned.csv', index=False)
print("\nCleaned dataset saved as 'All_Diets_cleaned.csv'")

# --- Visualization Section ---
print("\nGenerating visualizations...")

# Bar chart for average protein by diet type
plt.figure(figsize=(10, 5))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.xlabel('Diet Type')
plt.ylabel('Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('avg_protein_bar_chart.png')
plt.show()

# Scatter plot: Protein vs Carbs (top 5 protein-rich recipes)
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