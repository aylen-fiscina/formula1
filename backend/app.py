from flask import Flask, jsonify
from flask_cors import CORS
from db.formula1 import db, Piloto, Escuderia, Circuito

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://intro:intro@localhost:5432/formula1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello!'

@app.route('/pilotos', methods=['GET'])
def get_drivers():
    try:
        pilotos = Piloto.query.all()
        pilotos_data = []
        for driver in pilotos:
            driver_data = {
                'id': driver.id_piloto,
                'nombre': driver.nombre,
                'apellido': driver.apellido,
                'nacionalidad': driver.ciudad,
                'podios': driver.podios,
                'campeonatos_mundiales': driver.campeonatos_mundiales,
                'numero': driver.numero,
                'imagen': driver.imagen,
            }
            pilotos_data.append(driver_data)
        return jsonify({'pilotos': pilotos_data})
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500

@app.route('/escuderias', methods=['GET'])
def get_teams():
    try:
        escuderias = Escuderia.query.all()
        escuderias_data = []
        for escuderia in escuderias:
            escuderia_data = {
                'id': escuderia.id_escuderia,
                'campeonatos_mundiales': escuderia.campeonatos_mundiales,
                'nombre': escuderia.nombre,
                'lider': escuderia.lider,
                'imagen': escuderia.imagen,
                
            }
            escuderias_data.append(escuderia_data)
        return jsonify({'escuderias': escuderias_data})
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500
    
@app.route('/circuitos', methods=['GET'])
def get_races():
    try:
        circuitos = Circuito.query.all()
        circuitos_data = []
        for circuito in circuitos:
            circuito_data = {
                'id': circuito.id_circuito,
                'NombreCircuito': circuito.nombre,
                'Pais': circuito.ciudad,
                'Distancia': circuito.distancia,
                'imagen': circuito.imagen,
                #'Fecha': circuito.date.strftime('%Y-%m-%d'), 
            }
            circuitos_data.append(circuito_data)
        return jsonify({'circuitos': circuitos_data})  
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.run(host='localhost', port=5000, debug=True)
