import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Function to create the SQLite database and table if they don't exist
def init_db():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            task TEXT NOT NULL)''')
        conn.commit()

# Initialize the database when the app starts
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            conn.commit()
        return redirect('/')
    
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
    
    return render_template('index.html', tasks=tasks)

@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = request.form['task_id']
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
