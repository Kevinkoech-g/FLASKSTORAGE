from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/uploads/'
app.secret_key = 'supersecretkey'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Home route
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flash('File uploaded successfully!')
    return redirect(url_for('index'))

# Update route
@app.route('/update/<filename>', methods=['GET', 'POST'])
def update_file(filename):
    if request.method == 'POST':
        new_name = request.form['new_name']
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
        
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            flash('File renamed successfully!')
        else:
            flash('File not found!')

        return redirect(url_for('index'))
    return render_template('update.html', filename=filename)

# Delete route
@app.route('/delete/<filename>')
def delete_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        os.remove(path)
        flash('File deleted successfully!')
    else:
        flash('File not found!')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
