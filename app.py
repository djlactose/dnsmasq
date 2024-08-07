from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

HOSTS_FILE = '/etc/dnsmasq.d/hosts'
BACKUP_DIR = 'hosts_backup'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

def backup_hosts_file():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    with open(HOSTS_FILE, 'r') as file:
        content = file.read()
    backup_path = os.path.join(BACKUP_DIR, 'hosts.bak')
    with open(backup_path, 'w') as file:
        file.write(content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if User.query.first():
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = pbkdf2_sha256.hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and pbkdf2_sha256.verify(password, user.password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if User.query.count() == 0:
        return redirect(url_for('register'))
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        ip = request.form['ip']
        name = request.form['name']
        backup_hosts_file()
        with open(HOSTS_FILE, 'a') as file:
            file.write(f"{ip}\t{name}\n")
        return redirect(url_for('index'))
    
    with open(HOSTS_FILE, 'r') as file:
        content = file.readlines()
    
    return render_template('index.html', content=content)

@app.route('/remove/<int:line_number>', methods=['POST'])
def remove_entry(line_number):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    line_number = int(line_number)
    with open(HOSTS_FILE, 'r') as file:
        lines = file.readlines()
    if 0 <= line_number < len(lines):
        backup_hosts_file()
        del lines[line_number]
        with open(HOSTS_FILE, 'w') as file:
            file.writelines(lines)
    return redirect(url_for('index'))

@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    users = User.query.all()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            hashed_password = pbkdf2_sha256.hash(password)
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully', 'success')
        return redirect(url_for('manage_users'))
    return render_template('manage_users.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
    return redirect(url_for('manage_users'))

@app.route('/change_password/<int:user_id>', methods=['POST'])
def change_password(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if user:
        new_password = request.form['new_password']
        hashed_password = pbkdf2_sha256.hash(new_password)
        user.password = hashed_password
        db.session.commit()
        flash('Password changed successfully', 'success')
    return redirect(url_for('manage_users'))

def initialize_database():
    with app.app_context():
        db.create_all()

initialize_database()

if __name__ == '__main__':
    app.run(debug=True)
