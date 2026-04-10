import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # --- Task 1: Setup ---
    file_path = "data/trends_analysed.csv"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run Task 3 first.")
        return

    # Load the analyzed data
    df = pd.read_csv(file_path)
    
    # Create outputs directory if it doesn't exist
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Helper function to truncate long titles for cleaner charts
    def truncate_title(title):
        return title[:47] + "..." if len(str(title)) > 50 else title

    # --- Task 2: Chart 1 - Top 10 Stories by Score ---
    plt.figure(figsize=(10, 6))
    top_10 = df.nlargest(10, "score").sort_values("score", ascending=True)
    
    # Apply truncation to the titles for the Y-axis
    y_labels = [truncate_title(t) for t in top_10["title"]]
    
    plt.barh(y_labels, top_10["score"], color="skyblue")
    plt.xlabel("Score (Upvotes)")
    plt.title("Top 10 Stories by Score")
    plt.tight_layout() # Ensures labels don't get cut off
    plt.savefig(f"{output_dir}/chart1_top_stories.png")
    plt.close() # Close figure to free memory

    # --- Task 3: Chart 2 - Stories per Category ---
    plt.figure(figsize=(8, 6))
    cat_counts = df["category"].value_counts()
    
    # Use a built-in colormap to get different colors for each bar automatically
    colors = plt.cm.Paired(range(len(cat_counts)))
    
    cat_counts.plot(kind="bar", color=colors)
    plt.title("Number of Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Story Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/chart2_categories.png")
    plt.close()

    # --- Task 4: Chart 3 - Score vs Comments ---
    plt.figure(figsize=(8, 6))
    
    # Split the data to plot popular and non-popular stories in different colors
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    
    plt.scatter(not_popular["score"], not_popular["num_comments"], 
                alpha=0.6, label="Regular", color="gray")
    plt.scatter(popular["score"], popular["num_comments"], 
                alpha=0.7, label="Popular", color="orange", edgecolors="red")
    
    plt.title("Correlation: Score vs. Number of Comments")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig(f"{output_dir}/chart3_scatter.png")
    plt.close()

    # --- Bonus: Dashboard ---
    # We create a 2x2 grid (leaving one slot empty or spanning across)
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("TrendPulse Dashboard", fontsize=20, fontweight="bold")

    # Subplot 1: Top Stories (Horizontal Bar)
    axs[0, 0].barh(y_labels, top_10["score"], color="skyblue")
    axs[0, 0].set_title("Top 10 Stories")
    axs[0, 0].tick_params(axis='y', labelsize=8)

    # Subplot 2: Categories (Bar)
    axs[0, 1].bar(cat_counts.index, cat_counts.values, color=colors)
    axs[0, 1].set_title("Stories per Category")
    axs[0, 1].tick_params(axis='x', rotation=30)

    # Subplot 3: Score vs Comments (Scatter) - Spanning bottom row
    gs = axs[1, 0].get_gridspec()
    for ax in axs[1, :]:
        ax.remove()
    ax_big = fig.add_subplot(gs[1, :])
    
    ax_big.scatter(not_popular["score"], not_popular["num_comments"], color="gray", alpha=0.5, label="Regular")
    ax_big.scatter(popular["score"], popular["num_comments"], color="orange", alpha=0.7, label="Popular")
    ax_big.set_title("Engagement Analysis (Score vs. Comments)")
    ax_big.legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust for suptitle
    plt.savefig(f"{output_dir}/dashboard.png")
    plt.close()

    print(f"Visualizations complete. Check the '{output_dir}/' folder for results.")

if __name__ == "__main__":
    main()
