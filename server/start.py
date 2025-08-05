from flask import Flask, render_template, request, redirect, url_for
import opedm

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/search_components', methods=['GET', 'POST'])
def search_compontents():
    return render_template('search_components.html')

@app.route('/symbols', methods=['GET', 'POST'])
def symbols():
    return render_template('symbols.html')

@app.route('/footprints', methods=['GET', 'POST'])
def footprints():
    return render_template('footprints.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)