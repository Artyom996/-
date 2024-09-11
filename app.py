from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Получение значений переменных окружения
POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Конфигурация подключения к базе данных PostgreSQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@postgres.application.svc.cluster.local:5432/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Определение модели данных
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    startvac = db.Column(db.String(100), nullable=False)
    endvac = db.Column(db.String(100), nullable=False)

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

@app.route('/delete_contact/<int:id>', methods=['POST'])
def delete_contact(id):
    contact_to_delete = Contact.query.get_or_404(id)
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/all-data')
    except:
        return 'There was a problem deleting that contact'

@app.route('/all-data')
def all_data():
    contacts = Contact.query.all()
    
    # Подсчёт оставшихся дней отпуска
    remaining_vacation_days = {}
    total_vacation_days_per_year = 25
    
    # Группируем по имени и фамилии, считаем количество дней отпуска
    for contact in contacts:
        full_name = f"{contact.first_name} {contact.last_name}"
        start_date = datetime.strptime(contact.startvac, '%Y-%m-%d')
        end_date = datetime.strptime(contact.endvac, '%Y-%m-%d')
        vacation_days_taken = (end_date - start_date).days + 1  # +1 чтобы включить последний день
        
        if full_name in remaining_vacation_days:
            remaining_vacation_days[full_name] += vacation_days_taken
        else:
            remaining_vacation_days[full_name] = vacation_days_taken
    
    # Теперь вычисляем оставшиеся дни
    for full_name in remaining_vacation_days:
        remaining_vacation_days[full_name] = total_vacation_days_per_year - remaining_vacation_days[full_name]

    return render_template('all_data.html', contacts=contacts, remaining_vacation_days=remaining_vacation_days)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
