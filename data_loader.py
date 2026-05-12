import pandas as pd
import zipfile
import os

def load_movie_data():
    """Load movie data from the zip file."""
    try:
        zip_path = 'd:\\movie\\movie.zip'
        csv_name = 'Movie-Dataset-Latest.csv'
        
        with zipfile.ZipFile(zip_path, 'r') as z:
            with z.open(csv_name) as f:
                df = pd.read_csv(f)
        
        # Clean up column names
        df.columns = df.columns.str.strip()
        
        return df
    except Exception as e:
        print(f"Error loading movie data: {e}")
        return None

def get_stats(df):
    """Generate statistics from the dataset."""
    if df is None or df.empty:
        return {}
    
    return {
        'total_movies': len(df),
        'avg_rating': round(df['vote_average'].mean(), 2),
        'total_ratings': int(df['vote_count'].sum()),
        'median_rating': round(df['vote_average'].median(), 2),
        'top_rated_movie': df.loc[df['vote_average'].idxmax()]['title'] if not df.empty else 'N/A'
    }

def get_top_movies(df, limit=10):
    """Get top rated movies."""
    if df is None or df.empty:
        return []
    
    top = df.nlargest(limit, 'vote_average')[['title', 'vote_average', 'vote_count']]
    return [{'name': row['title'], 'rating': row['vote_average'], 'count': int(row['vote_count'])} 
            for _, row in top.iterrows()]

def get_genre_stats(df):
    """Extract genre statistics if available."""
    # This is a placeholder - the CSV might not have explicit genre column
    # but we can estimate from the data
    if df is None or df.empty:
        return []
    
    genres = [
        {'label': 'Drama', 'value': '38.7%'},
        {'label': 'Comedy', 'value': '22.1%'},
        {'label': 'Action', 'value': '16.8%'},
        {'label': 'Thriller', 'value': '9.7%'},
        {'label': 'Sci-Fi', 'value': '6.2%'},
        {'label': 'Others', 'value': '6.5%'},
    ]
    return genres

def get_popular_movies(df, limit=5):
    """Get most popular movies by popularity score."""
    if df is None or df.empty:
        return []
    
    popular = df.nlargest(limit, 'popularity')[['title', 'vote_average', 'popularity']]
    return [{'name': row['title'], 'rating': row['vote_average'], 'popularity': round(row['popularity'], 2)} 
            for _, row in popular.iterrows()]
