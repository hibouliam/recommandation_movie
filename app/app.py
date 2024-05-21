# Flask app that needs to serve static files (HTML, CSS and JS)
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('notation'))

@app.route('/proposition')
def proposition():
    return render_template('proposition.html')

@app.route('/voir_apres')
def voir_apres():
    return render_template('voir_apres.html')

@app.route('/notation')
def notation():
    return render_template('notation.html')

@app.route('/soon_available')
def soon_available():
    return render_template('soon_available.html')


if __name__ == "__main__":
    # Changer le port ici
    port = 5001  # Ou tout autre numéro de port que vous souhaitez utiliser
    app.run(port=port)