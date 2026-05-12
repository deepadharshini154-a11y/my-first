from flask import Flask, render_template, request, redirect, url_for, session
from data_loader import load_movie_data, get_stats, get_top_movies, get_popular_movies

app = Flask(__name__)
app.secret_key = 'dev'

ratings = []
movie_df = load_movie_data()

def logged_in():
    return session.get('user') is not None

@app.route('/')
def home():
    return render_template('home.html', user=session.get('user'))

@app.route('/ratings', methods=['GET', 'POST'])
def ratings_page():
    if not logged_in():
        return redirect(url_for('login'))
    if request.method == 'POST':
        movie = request.form.get('movie', '').strip()
        score = request.form.get('score', '').strip()
        if movie and score:
            ratings.append({'movie': movie, 'score': score})
        return redirect(url_for('ratings_page'))
    return render_template('index.html', ratings=ratings)

def render_section(page_key, title, subtitle, description, cards, rows=None):
    if not logged_in():
        return redirect(url_for('login'))
    page = {
        'key': page_key,
        'title': title,
        'subtitle': subtitle,
        'description': description,
        'cards': cards,
        'rows': rows or []
    }
    return render_template('section.html', page=page)

@app.route('/genres')
def genres():
    cards = [{'label': 'Drama', 'value': '38.7%'}, {'label': 'Comedy', 'value': '22.1%'}, {'label': 'Action', 'value': '16.8%'}]
    rows = [{'name': 'Drama', 'detail': 'Highest share', 'value': '38.7%'}, {'name': 'Comedy', 'detail': 'Popular genre', 'value': '22.1%'}, {'name': 'Action', 'detail': 'Growing category', 'value': '16.8%'}]
    return render_section('genres', 'Genres', 'Explore movie genres', 'Browse genre distribution insights.', cards, rows)

@app.route('/directors')
def directors():
    cards = [{'label': 'Christopher Nolan', 'value': '8.15'}, {'label': 'Martin Scorsese', 'value': '7.98'}, {'label': 'Steven Spielberg', 'value': '7.90'}]
    rows = [{'name': 'Christopher Nolan', 'detail': '20 movies', 'value': '8.15'}, {'name': 'Martin Scorsese', 'detail': '35 movies', 'value': '7.98'}, {'name': 'Steven Spielberg', 'detail': '31 movies', 'value': '7.90'}]
    return render_section('directors', 'Directors', 'Top directors', 'Review director ratings.', cards, rows)

@app.route('/actors')
def actors():
    return render_section(
        'actors',
        'Actors',
        'Explore actor ratings and appearances',
        'View actor performance metrics and popular film participation.',
        [
            {'label': 'Robert Downey Jr.', 'value': '8.2'},
            {'label': 'Meryl Streep', 'value': '8.0'},
            {'label': 'Leonardo DiCaprio', 'value': '8.1'}
        ],
        [
            {'name': 'Leonardo DiCaprio', 'detail': 'Top rated actor', 'value': '8.1'},
            {'name': 'Meryl Streep', 'detail': 'Highly versatile', 'value': '8.0'},
            {'name': 'Robert Downey Jr.', 'detail': 'Popular films', 'value': '8.2'}
        ]
    )

@app.route('/users')
def users():
    return render_section(
        'users',
        'Users',
        'User activity and ratings distribution',
        'Analyze user behavior, ratings per user, and engagement patterns.',
        [
            {'label': 'Active users', 'value': '1,234,567'},
            {'label': 'Ratings per user', 'value': '16.5'},
            {'label': 'Top rater', 'value': '3,245'}
        ],
        [
            {'name': '1-2', 'detail': 'Low engagement', 'value': '8.2%'},
            {'name': '2-5', 'detail': 'Most users', 'value': '24.7%'},
            {'name': '6-10', 'detail': 'Highly active', 'value': '21.5%'}
        ]
    )

@app.route('/lists')
def lists():
    return render_section(
        'lists',
        'Lists',
        'Curated movie lists and collections',
        'Manage and explore curated movie lists for easy discovery.',
        [
            {'label': 'Top 10', 'value': '5 lists'},
            {'label': 'New releases', 'value': '3 lists'},
            {'label': 'Classic films', 'value': '4 lists'}
        ],
        [
            {'name': 'Top 10', 'detail': 'Highest rated', 'value': '5 lists'},
            {'name': 'New releases', 'detail': 'Trending now', 'value': '3 lists'},
            {'name': 'Classic films', 'detail': 'All-time favorites', 'value': '4 lists'}
        ]
    )

@app.route('/recommendations')
def recommendations():
    popular = get_popular_movies(movie_df, 5)
    cards = [{'label': 'Recommended', 'value': str(len(popular))} if popular else {'label': 'Recommended', 'value': '25'}]
    rows = [{'name': m['name'], 'detail': 'Top rated', 'value': str(m['rating'])} for m in popular[:5]]
    return render_section('recommendations', 'Recommendations', 'Popular movies', 'Based on ratings and popularity.', cards, rows)

@app.route('/reports')
def reports():
    return render_section(
        'reports',
        'Reports',
        'Analytic summaries and export-ready reports',
        'Generate and review reports for ratings, genres, and user behavior.',
        [
            {'label': 'Monthly reports', 'value': '4 ready'},
            {'label': 'Top charts', 'value': '3 available'},
            {'label': 'Export data', 'value': 'CSV / JSON'}
        ],
        [
            {'name': 'Monthly ratings', 'detail': 'Performance snapshot', 'value': '4 reports'},
            {'name': 'Genre trends', 'detail': 'Top categories', 'value': '3 reports'},
            {'name': 'User activity', 'detail': 'Engagement insights', 'value': '2 reports'}
        ]
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        return redirect(url_for('dashboard'))

    message = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        if email == 'deepa@gmail.com' and password == 'deepa123':
            session['user'] = email
            return redirect(url_for('dashboard'))
        message = 'Invalid email or password. Use deepa@gmail.com / deepa123.'
    return render_template('login.html', message=message)

@app.route('/dashboard')
def dashboard():
    if not logged_in():
        return redirect(url_for('login'))
    stats = get_stats(movie_df)
    top_movies = get_top_movies(movie_df, 5)
    return render_template('dashboard.html', stats=stats, top_movies=top_movies)

@app.route('/movielens')
def movielens():
    if not logged_in():
        return redirect(url_for('login'))
    return render_template('movielens.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
