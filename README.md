# Netflix Data Analysis Dashboard

An interactive web application built with Streamlit that provides comprehensive analysis and visualization of Netflix content data.

## Features

- 📊 **Overview Dashboard**

  - Total content metrics
  - Distribution of movies vs. TV shows
  - Rating distribution analysis

- 🎭 **Content Analysis**

  - Interactive genre exploration
  - Top genres visualization
  - Genre insights and statistics

- 📈 **Trends Over Time**

  - Yearly content addition trends
  - Monthly distribution patterns
  - Content growth analysis by type

- 👥 **Directors & Creators**

  - Top directors visualization
  - Content distribution by country
  - Interactive treemap visualizations

- 🔍 **Word Cloud Analysis**
  - Movie titles word cloud
  - TV show titles word cloud
  - Title length distribution analysis

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- WordCloud
- Plotly

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
```

2. Install required packages:

```bash
pip install streamlit pandas numpy matplotlib seaborn wordcloud plotly
```

3. Navigate to the project directory:

```bash
cd netflix_data_analysis
```

4. Run the Streamlit app:

```bash
streamlit run netflix_data_analysis.py
```

## Data Source

The analysis is performed on the `netflix1.csv` dataset, which should be placed in the same directory as the script. The dataset contains information about Netflix content including titles, directors, cast, release years, ratings, and more.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

[Your Name]

## Acknowledgments

- Netflix for providing the inspiration
- Streamlit for the amazing framework
- The data science community for continuous support
