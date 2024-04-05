from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@db/mydatabase'

db = SQLAlchemy(app)

class Paquete(db.Model):
    id_paquete = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50))


paquetes = {} #TODO: Cambiar a una base de datos

@app.route('/paquetes', methods=['GET'])
def get_paquetes():
    return jsonify(paquetes)

@app.route('/paquete', methods=['POST'])
def registrar_paquete():
    datos = request.json
    id_paquete = datos['id']
    paquetes[id_paquete] = {'estado': 'registrado'}
    return jsonify({'mensaje': 'Paquete registrado con éxito'}), 201

@app.route('/paquete/<id>', methods=['GET'])
def obtener_estado_paquete(id):
    paquete = paquetes.get(id)
    if paquete:
        return jsonify({'id': id, 'estado': paquete['estado']})
    else:
        return jsonify({'mensaje': 'Paquete no encontrado'}), 404
    
@app.route('/paquete/<id>', methods=['PUT'])
def actualizar_estado_paquete(id):
    datos = request.json
    estado = datos.get('estado')
    if id in paquetes:
        paquetes[id]['estado'] = estado
        return jsonify({'mensaje': 'Estado actualizado'})
    else:
        return jsonify({'mensaje': 'Paquete no encontrado'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
