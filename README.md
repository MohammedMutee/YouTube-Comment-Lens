# YouTube Comment Lens

A Python Streamlit application that analyzes YouTube video comments to provide sentiment analysis and channel statistics.

## Features
-   **Sentiment Analysis**: Categorizes comments into Positive, Negative, and Neutral.
-   **Visualizations**: Interactive bar charts and pie charts of sentiment distribution.
-   **Channel Stats**: Displays subscriber count, total videos, and channel description.
-   **Data Export**: Download scraped comments as CSV.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/YouTube-Comment-Lens.git
    cd YouTube-Comment-Lens
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**:
    -   Create a file `.streamlit/secrets.toml`.
    -   Add your YouTube Data API key:
        ```toml
        [general]
        API_KEY = "YOUR_API_KEY_HERE"
        ```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```
Enter a YouTube video URL in the sidebar to analyze comments.

## Tech Stack
-   Python
-   Streamlit
-   YouTube Data API v3
-   NLTK (VADER Sentiment)
-   Plotly
