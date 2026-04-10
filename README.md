
# TrendPulse: What's Actually Trending Right Now

A full-stack Python data pipeline that fetches live stories from HackerNews, cleans the data, performs statistical analysis, and generates a visual dashboard of current trends.

## Project Structure
The project is divided into four main tasks:
1. **`task1_data_collection.py`**: Fetches and categorizes raw JSON data.
2. **`task2_data_processing.py`**: Cleans data and exports to CSV.
3. **`task3_analysis.py`**: Calculates statistics and feature engineering.
4. **`task4_visualization.py`**: Generates charts and a final dashboard.

---

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   pip install requests pandas numpy matplotlib
   ```

2. **Run the Pipeline (In order):**
   ```bash
   python task1_data_collection.py
   python task2_data_processing.py
   python task3_analysis.py
   python task4_visualization.py
   ```

---

## 🛠 How It Works

### Task 1: Data Collection
* **Source:** Pulls the top 500 story IDs from the HackerNews API.
* **Categorization:** Matches titles against keywords for 5 categories (Tech, World News, Sports, Science, Entertainment).
* **Rate Limiting:** Pauses for 2 seconds between categories to remain API-friendly.
* **Output:** `data/trends_YYYYMMDD.json`

### Task 2: Data Processing
* **Cleaning:** Removes duplicates based on `post_id` and drops rows with missing critical fields.
* **Filtering:** Removes "low quality" stories with scores lower than 5.
* **Normalization:** Strips whitespace from titles and ensures correct integer types for scores and comments.
* **Output:** `data/trends_clean.csv`

### Task 3: Analysis with Pandas & NumPy
* **Statistics:** Uses NumPy to calculate the mean, median, and standard deviation of upvotes.
* **Feature Engineering:** Adds two new metrics:
    * `engagement`: Calculated as `num_comments / (score + 1)`.
    * `is_popular`: A boolean flag for stories performing above the average score.
* **Output:** `data/trends_analysed.csv`

### Task 4: Visualizations
* **Chart 1:** Top 10 stories by score (Horizontal Bar).
* **Chart 2:** Story distribution across categories (Categorical Bar).
* **Chart 3:** Engagement analysis (Score vs. Comments Scatter Plot).
* **Dashboard:** A combined summary of all metrics.
* **Output:** `outputs/*.png`

---

## 📊 Final Output
After running the full pipeline, you will find a generated dashboard in the `outputs/` folder:

* **`chart1_top_stories.png`**
* **`chart2_categories.png`**
* **`chart3_scatter.png`**
* **`dashboard.png`**

---

**Author:** vani goswami
THANK YOU
