from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


#  LOGIN ROUTES 

@app.route('/')
def login_page():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        return "Username and password are required.", 400

    # Open DB connection
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row

    user = conn.execute(
        "SELECT * FROM user_info WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()

    conn.close()

    if user:
        return redirect(url_for('main_page'))
    else:
        return "Invalid username or password.", 401



#  MAIN TASK LIST 

@app.route('/main')
def main_page():
    # Open DB connection
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row

    tasks = conn.execute("SELECT * FROM tasks").fetchall()

    conn.close()

    return render_template('main.html', tasks=tasks)



#  ADD TASK 

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        done = request.form.get('done', '0').strip()

        if not title:
            return "Title cannot be empty.", 400

        if len(title) < 3:
            return "Title must be at least 3 characters.", 400

        if done not in ['0', '1']:
            return "Done must be 0 or 1.", 400

        # Open DB connection
        conn = sqlite3.connect('tasks.db')
        conn.row_factory = sqlite3.Row

        conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (title, int(done))
        )
        conn.commit()
        conn.close()

        return redirect(url_for('main_page'))

    # GET
    return render_template('add_task.html')



#  UPDATE TASK 

@app.route('/update/<int:id>', methods=['GET'])
def show_update_form(id):
    # Open DB connection
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if task is None:
        return "Task not found.", 404

    return render_template('update.html', task=task)


@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    title = request.form.get('title', '').strip()
    done = request.form.get('done', '0').strip()

    if not title:
        return "Title cannot be empty.", 400

    if len(title) < 3:
        return "Title must be at least 3 characters.", 400

    if done not in ['0', '1']:
        return "Done must be 0 or 1.", 400

    # Open DB connection
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row

    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, int(done), id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('main_page'))



# DELETE TASK 
@app.route('/delete/<int:id>')
def delete_task(id):
    # Open DB connection
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row

    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('main_page'))



# RUN APP 

if __name__ == '__main__':
    app.run(debug=True)
