import pandas as pd
import numpy as np
import os

def main():
    # --- Task 1: Load and Explore ---
    file_path = "data/trends_clean.csv"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run Task 2 first.")
        return

    # Load the clean CSV
    df = pd.read_csv(file_path)

    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())

    # Calculate averages using Pandas
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"\nAverage score   : {avg_score:,.2f}")
    print(f"Average comments: {avg_comments:,.2f}")

    # --- Task 2: Basic Analysis with NumPy ---
    print("\n--- NumPy Stats ---")
    
    # Extracting columns as NumPy arrays for processing
    scores = df["score"].to_numpy()
    comments = df["num_comments"].to_numpy()
    categories = df["category"].to_numpy()

    # 1. Score Statistics
    print(f"Mean score   : {np.mean(scores):,.2f}")
    print(f"Median score : {np.median(scores):,.2f}")
    print(f"Std deviation: {np.std(scores):,.2f}")
    print(f"Max score    : {np.max(scores):,}")
    print(f"Min score    : {np.min(scores):,}")

    # 2. Category with most stories
    # We use np.unique to count occurrences and np.argmax to find the peak
    unique_cats, counts = np.unique(categories, return_counts=True)
    most_common_idx = np.argmax(counts)
    print(f"Most stories in: {unique_cats[most_common_idx]} ({counts[most_common_idx]} stories)")

    # 3. Story with most comments
    # Find the index of the maximum value in the comments array
    max_comment_idx = np.argmax(comments)
    top_story_title = df.iloc[max_comment_idx]["title"]
    top_story_count = df.iloc[max_comment_idx]["num_comments"]
    print(f"Most commented story: \"{top_story_title}\" — {top_story_count:,} comments")

    # --- Task 3: Add New Columns ---
    
    # Calculate engagement: Discussion per upvote
    # Adding 1 to the denominator avoids DivisionByZero errors
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # Boolean flag: Is the story above the average score?
    df["is_popular"] = df["score"] > avg_score

    # --- Task 4: Save the Result ---
    
    output_file = "data/trends_analysed.csv"
    try:
        df.to_csv(output_file, index=False)
        print(f"\nSaved to {output_file}")
    except Exception as e:
        print(f"Failed to save analyzed data: {e}")

if __name__ == "__main__":
    main()
