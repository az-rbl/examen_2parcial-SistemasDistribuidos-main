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


@app.route('/')
def hello():
    # Create the tables if they don't exist
    db.create_all()

@app.route('/paquetes', methods=['GET'])
def get_paquetes():
    paquetes = Paquete.query.all()
    resultado = []
    for paquete in paquetes:
        paquete_datos ={'id_paquete': paquete.id_paquete, 'estado': paquete.estado}
        resultado.append(paquete_datos)
    return jsonify(resultado)

@app.route('/paquete', methods=['POST'])
def registrar_paquete():
    datos = request.get_json()
    id = datos.get('id')
    db.session.add(Paquete(id_paquete=id, estado='registrado'))
    db.session.commit()
    return jsonify({'mensaje': 'Paquete registrado con éxito'}), 200

@app.route('/paquete/<id>', methods=['GET'])
def obtener_estado_paquete(id):
    paquete = Paquete.query.get(id)
    if paquete:
        return jsonify({'id': id, 'estado': paquete.estado})
    else:
        return jsonify({'mensaje': 'Paquete no encontrado'}), 404
    
@app.route('/paquete/<id>', methods=['PUT'])
def actualizar_estado_paquete(id):
    datos = request.get_json()
    estado = datos.get('estado')
    paquete = Paquete.query.get(id)
    if paquete:
        paquete.estado = estado
        db.session.commit()
        return jsonify({'mensaje': 'Estado actualizado'})
    else:
        return jsonify({'mensaje': 'Paquete no encontrado'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
