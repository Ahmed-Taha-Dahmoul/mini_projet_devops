from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration de la base de données SQLite
# Le fichier sera stocké dans un dossier 'instance'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'etudiants.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de données
class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)

# Création de la base de données au démarrage
with app.app_context():
    if not os.path.exists('instance'):
        os.makedirs('instance')
    db.create_all()

@app.route('/')
def index():
    total = Etudiant.query.count()
    return render_template('index.html', total=total)

@app.route('/liste')
def liste():
    etudiants = Etudiant.query.all()
    return render_template('liste.html', etudiants=etudiants)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        nouveau_nom = request.form.get('nom')
        nouveau_prenom = request.form.get('prenom')
        nouvel_etu = Etudiant(nom=nouveau_nom, prenom=nouveau_prenom)
        db.session.add(nouvel_etu)
        db.session.commit()
        return redirect(url_for('liste'))
    return render_template('ajouter.html')

@app.route('/supprimer/<int:id>')
def supprimer(id):
    etu = Etudiant.query.get_or_404(id)
    db.session.delete(etu)
    db.session.commit()
    return redirect(url_for('liste'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)