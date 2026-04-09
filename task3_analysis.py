# task3_analysis.py

# Import required libraries
import pandas as pd
import numpy as np

# -------------------------------
# 1. Load and Explore the Data
# -------------------------------

# Load the cleaned CSV file
df = pd.read_csv("data/trends_clean.csv")

# Print first 5 rows
print("First 5 rows:")
print(df.head())

# Print shape of the DataFrame
print("\nLoaded data:", df.shape)

# Calculate average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score   :", int(avg_score))
print("Average comments:", int(avg_comments))


# -------------------------------
# 2. Basic Analysis with NumPy
# -------------------------------

# Convert columns to NumPy arrays
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

print("\n--- NumPy Stats ---")

# Mean, Median, Standard Deviation
print("Mean score   :", int(np.mean(scores)))
print("Median score :", int(np.median(scores)))
print("Std deviation:", int(np.std(scores)))

# Max and Min
print("Max score    :", np.max(scores))
print("Min score    :", np.min(scores))

# Category with most stories
most_common_category = df["category"].value_counts().idxmax()
count_category = df["category"].value_counts().max()

print("\nMost stories in:", most_common_category, f"({count_category} stories)")

# Story with most comments
max_comments_index = np.argmax(comments)

top_story_title = df.loc[max_comments_index, "title"]
top_story_comments = df.loc[max_comments_index, "num_comments"]

print("\nMost commented story:")
print(f'"{top_story_title}" — {top_story_comments} comments')


# -------------------------------
# 3. Add New Columns
# -------------------------------

# Engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average score
df["is_popular"] = df["score"] > avg_score


# -------------------------------
# 4. Save the Result
# -------------------------------

# Save the updated DataFrame
df.to_csv("data/trends_analysed.csv", index=False)

print("\nSaved to data/trends_analysed.csv")