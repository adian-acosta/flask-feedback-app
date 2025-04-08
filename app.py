from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('feedback.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL
                )
            ''')

# Route for the home page
@app.route('/')
def home():
    with sqlite3.connect('feedback.db') as conn:
        feedbacks = conn.execute('SELECT name, message FROM feedback').fetchall()
    return render_template('home.html', feedbacks=feedbacks)

# Route for submitting feedback
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        with sqlite3.connect('feedback.db') as conn:
            conn.execute('INSERT INTO feedback (name, message) VALUES (?, ?)', (name, message))
        return redirect('/')
    return render_template('submit.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)