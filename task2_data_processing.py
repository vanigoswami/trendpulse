import pandas as pd
import glob
import os

def main():
    # --- Task 1: Load the JSON File ---
    json_files = glob.glob("data/trends_*.json")
    
    if not json_files:
        print("Error: No JSON data file found in the 'data/' directory.")
        return

    # Select the most recent file if multiple exist
    input_file = max(json_files, key=os.path.getctime)
    
    df = pd.DataFrame()
    try:
        df = pd.read_json(input_file)
        print(f"Loaded {len(df)} stories from {input_file}")
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return

    # --- Task 2: Clean the Data ---
    
    # 1. Remove Duplicates: Ensure each post_id is unique
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # 2. Missing Values: Drop rows where essential fields are null
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # 3. Data Types: Convert score and num_comments to integers
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # 4. Low Quality: Keep only stories with a score of 5 or higher
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 5. Whitespace: Clean up the titles
    df["title"] = df["title"].str.strip()

    # --- Task 3: Save as CSV & Summary ---
    
    output_path = "data/trends_clean.csv"
    try:
        # Save to CSV without the index column
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} rows to {output_path}")
        
        # Quick Summary: Count stories per category
        print("\nStories per category:")
        summary = df["category"].value_counts()
        print(summary.to_string())
        
    except Exception as e:
        print(f"Failed to save CSV: {e}")

if __name__ == "__main__":
    main()
