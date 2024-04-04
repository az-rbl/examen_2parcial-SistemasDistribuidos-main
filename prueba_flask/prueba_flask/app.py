import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Utiliza variables de entorno para configurar la conexión a PostgreSQL
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')
db_host = os.getenv('POSTGRES_HOST')  # Nombre del servicio en docker-compose
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@db/{db_name}'

db = SQLAlchemy(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Ruta para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    nombre = request.json['nombre']
    nuevo_usuario = Usuario(nombre=nombre)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado exitosamente'}), 201

# Ruta para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    resultado = []
    for usuario in usuarios:
        usuario_data = {'id': usuario.id, 'nombre': usuario.nombre}
        resultado.append(usuario_data)
    return jsonify(resultado)

@app.route('/')
def hola_mundo():
    return 'Hola Mundo'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
