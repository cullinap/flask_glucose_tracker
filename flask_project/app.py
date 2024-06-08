from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Float, nullable=False)
    blood_glucose = db.Column(db.Float, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        timestamp = request.form['timestamp']
        weight = request.form['weight']
        blood_glucose = request.form['blood_glucose']

        if timestamp and weight and blood_glucose:
            new_entry = Entry(
                timestamp=datetime.strptime(timestamp, '%Y-%m-%dT%H:%M'),
                weight=float(weight),
                blood_glucose=float(blood_glucose)
            )
            with app.app_context():
                db.session.add(new_entry)
                db.session.commit()
            return redirect(url_for('index'))
    
    with app.app_context():
        entries = Entry.query.order_by(Entry.timestamp.desc()).all()
    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
