# Movie-dashboard
A dashboard for movie data using Streamlit, Plotly, and other libraries.

🎬 Movie Dashboard is a data-driven web application that provides insightful visualizations about movies, including genres, ratings, top actors, and popular keywords. This interactive dashboard lets users filter movies based on various criteria and view the top-rated movies with dynamic charts.

**Features**
Filter movies by genre: Choose from a variety of genres to see the top-rated movies.

Minimum number of votes slider: Refine results based on the minimum number of votes a movie must have.

Minimum rating slider: Filter movies based on a minimum rating.

Top actors: See the most frequent actors in a selected genre.

Top keywords: View the most common keywords associated with movies in the selected genre.

**Technologies Used**
Streamlit: For building the web interface.

Plotly: For creating interactive charts and visualizations.

Pandas: For data manipulation and analysis.

CSV files: Using real movie data from multiple CSV files like movies_metadata.csv, credits.csv, keywords.csv.

**Installation**
To run this project locally, follow these steps:

1.Clone this repository:
git clone https://github.com/your-username/movie-dashboard.git
cd movie-dashboard

2.Set up a Python virtual environment (optional but recommended):
python -m venv venv

3.Activate the virtual environment:
For Windows:
venv\Scripts\activate

For macOS/Linux:
source venv/bin/activate

4.Install the required dependencies:
pip install -r requirements.txt

5.Run the Streamlit app:
streamlit run movie_dashboard.py

6.Open your browser and go to http://localhost:8501 to view the app.

**How to Use**
Select a genre from the dropdown menu.
Use the sliders to filter movies by minimum number of votes and rating.
See the visualizations of top-rated movies, top actors, and top keywords.

**Contributing**
Feel free to open issues or submit pull requests if you find any bugs or have improvements to suggest!
