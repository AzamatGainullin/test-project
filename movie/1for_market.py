from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pandas as pd
from sklearn.externals import joblib
from flask_sqlalchemy import SQLAlchemy

#определяем приложение для запуска с характеристиками базы данных (путь, имя, шаблон таблицы для запроса)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///1test.db'
db = SQLAlchemy(app)
class ITEMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, nullable=False)
    High = db.Column(db.FLOAT, unique=False, nullable=False)
    Low = db.Column(db.FLOAT, unique=False, nullable=False)
    company = db.Column(db.String(80), unique=False, nullable=False)
    def __repr__(self):
        return "(%r, %r, %r, %r)" % (self.Date, self.High, self.Low, self.company)
    def to_dict(self):
        return {'Date':self.Date, 'High':self.High, 'Low':self.Low,
               'company':self.company}

#загружаем traindata_standard
traindata_standard=joblib.load('1traindata_standard_03_07_2019__10_07_2019.pkl')
ts = traindata_standard['FBHS'].tail()


#загружаем item из базы данных db по запросу-фильтру, и трансформируем в example - тип DataFrame
item = ITEMS.query.filter_by(company='FBHS').all()
example = pd.DataFrame([i.to_dict() for i in item])
example.index = example['Date']
example.drop('Date',axis=1,inplace=True)
ex = example.head()

@app.route('/example_1')
def example_1():
    return ex.to_html()

@app.route('/example_2')
def example_2():
    return ts.to_html()



if __name__ == '__main__':
    app.run(debug=True)
