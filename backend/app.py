from flask import Flask, jsonify
from flask_cors import CORS
from db.formula1 import db, Drivers, Escuderias  

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
        pilotos = Drivers.query.all()
        pilotos_data = []
        for driver in pilotos:
            driver_data = {
                'id': driver.id_piloto,
                'Nombre': driver.firstName,
                'Apellido': driver.lastName,
                'Nacionalidad': driver.city,
                'Equipo': driver.team,
                'Podios': driver.podiums,
                'Campeonatos Mundiales': driver.world_championships_piloto,
                'Numero': driver.number_piloto,
            }
            pilotos_data.append(driver_data)
        return jsonify({'pilotos': pilotos_data})
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500

@app.route('/escuderias', methods=['GET'])
def get_teams():
    try:
        escuderias = Escuderias.query.all()
        escuderias_data = []
        for escuderia in escuderias:
            escuderia_data = {
                'id': escuderia.id_team,
                'Campeonatos Mundiales': escuderia.world_championships_team,
                'Nombre Escuderia': escuderia.full_team_name,
                'Jefe de Equipo': escuderia.team_chief,
            }
            escuderias_data.append(escuderia_data)
        return jsonify({'escuderias': escuderias_data})
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
        print("Tables created successfully!")
    app.run(host='localhost', port=5000, debug=True)
