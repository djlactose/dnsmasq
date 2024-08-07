from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

HOSTS_FILE = '/etc/dnsmasq.d/hosts'  # Updated path
BACKUP_DIR = 'hosts_backup'

def backup_hosts_file():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    with open(HOSTS_FILE, 'r') as file:
        content = file.read()
    backup_path = os.path.join(BACKUP_DIR, 'hosts.bak')
    with open(backup_path, 'w') as file:
        file.write(content)

@app.route('/', methods=['GET', 'POST'])
def index():
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
    line_number = int(line_number)
    with open(HOSTS_FILE, 'r') as file:
        lines = file.readlines()
    if 0 <= line_number < len(lines):
        backup_hosts_file()
        del lines[line_number]
        with open(HOSTS_FILE, 'w') as file:
            file.writelines(lines)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
