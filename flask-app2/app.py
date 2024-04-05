from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@db:5432/mydatabase'

db = SQLAlchemy(app)

class Paquete(db.Model):
    id_paquete = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50))
    


#paquetes = {} #TODO: Cambiar a una base de datos


@app.route('/contar', methods=['GET'])
def contar():
    count = Paquete.query.count()
    return jsonify(paquetes=count)

@app.route('/distintos', methods=['GET'])
def distintos_estados():
    distintos_estados = db.session.query(Paquete.estado).distinct().all()
    return jsonify([status[0] for status in distintos_estados])

@app.route('/resumen', methods=['GET'])
def get_status_summary():
    summary = db.session.query(Paquete.estado, db.func.count(Paquete.estado).label('count')).group_by(Paquete.estado).all()
    return jsonify({status: count for status, count in summary})
    
if __name__ == '__main__':
    app.run(debug=True)
