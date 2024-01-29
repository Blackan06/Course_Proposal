# run.py
from flask import Flask , render_template
from app import create_app

app = create_app()

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
