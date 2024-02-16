from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_automatic_mode')
def start_automatic_mode():
    return 'Automatic mode started'

@app.route('/start_manual_mode')
def start_manual_mode():
    return 'Manual mode started'

if __name__ == '__main__':
    app.run(debug=True)
