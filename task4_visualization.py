# Task 4 — Visualizations
# TrendPulse Project

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# STEP 1: Load Data
# -------------------------------
df = pd.read_csv("data/trends_analysed.csv")

# -------------------------------
# STEP 2: Create outputs folder
# -------------------------------
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# -------------------------------
# STEP 3: Chart 1 - Top 10 Stories by Score
# -------------------------------

# Sort by score and take top 10
top_stories = df.sort_values(by="score", ascending=False).head(10)

# Shorten titles to max 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

plt.figure(figsize=(10, 6))

# Horizontal bar chart
plt.barh(top_stories["short_title"], top_stories["score"])

plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

# Invert y-axis for better readability
plt.gca().invert_yaxis()

# Save before show
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# -------------------------------
# STEP 4: Chart 2 - Stories per Category
# -------------------------------

# Count stories per category
category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))

# Bar chart with different colors
plt.bar(category_counts.index, category_counts.values, color=plt.cm.tab10.colors)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.savefig("outputs/chart2_categories.png")
plt.close()

# -------------------------------
# STEP 5: Chart 3 - Score vs Comments
# -------------------------------

plt.figure(figsize=(8, 5))

# Separate popular and non-popular
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

# Scatter plot
plt.scatter(popular["score"], popular["num_comments"], color="green", label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], color="red", label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")

plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.close()

# -------------------------------
# BONUS: Dashboard (All Charts Together)
# -------------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 in dashboard
axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].set_title("Top Stories")
axes[0].invert_yaxis()

# Chart 2 in dashboard
axes[1].bar(category_counts.index, category_counts.values, color=plt.cm.tab10.colors)
axes[1].set_title("Categories")

# Chart 3 in dashboard
axes[2].scatter(popular["score"], popular["num_comments"], color="green", label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], color="red", label="Not Popular")
axes[2].set_title("Score vs Comments")

# Overall title
plt.suptitle("TrendPulse Dashboard")

# Save dashboard
plt.savefig("outputs/dashboard.png")
plt.close()

print("All charts saved successfully in 'outputs/' folder!")