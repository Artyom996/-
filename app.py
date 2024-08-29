from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Конфигурация подключения к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@postgres.application.svc.cluster.local:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Определение модели данных
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

# Создание таблицы в базе данных
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    startvac = request.form['startvac']
    endvac = request.form['endvac']

    new_contact = Contact(first_name=first_name, last_name=last_name, startvac=startvac, endvac=endvac)
    db.session.add(new_contact)
    db.session.commit()

    return redirect('/all-data')

@app.route('/all-data')
def all_data():
    contacts = Contact.query.all()  # Извлекаем все контакты из базы данных
    return render_template('all_data.html', contacts=contacts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
