from flask import Flask, jsonify, request
from flask_cors import CORS
from db.formula1 import db, Piloto, Escuderia, Circuito, Carrera

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
        pilotos = db.session.query(Piloto, Escuderia).join(Escuderia, Piloto.id_escuderia == Escuderia.id_escuderia).all()
        pilotos_data = []
        for piloto, escuderia in pilotos:
            driver_data = {
                'id': piloto.id_piloto,
                'nombre': piloto.nombre,
                'apellido': piloto.apellido,
                'equipo': escuderia.nombre,  
                'nacionalidad': piloto.ciudad,
                'podios': piloto.podios,
                'campeonatos_mundiales': piloto.campeonatos_mundiales,
                'numero': piloto.numero,
                'imagen': piloto.imagen,
            }
            pilotos_data.append(driver_data)
        return jsonify({'pilotos': pilotos_data})
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500

@app.route('/pilotos/<int:id_piloto>', methods=['GET'])
def get_driver(id_piloto):
    try:
        piloto, escuderia = db.session.query(Piloto, Escuderia).join(Escuderia, Piloto.id_escuderia == Escuderia.id_escuderia).filter(Piloto.id_piloto == id_piloto).first()
        
        if not piloto:
            return jsonify({'message': 'Piloto no encontrado'}), 404
    
        driver_data = {
            'id': piloto.id_piloto,
            'nombre': piloto.nombre,
            'apellido': piloto.apellido,
            'equipo': escuderia.nombre,
            'nacionalidad': piloto.ciudad,
            'podios': piloto.podios,
            'campeonatos_mundiales': piloto.campeonatos_mundiales,
            'numero': piloto.numero,
            'imagen': piloto.imagen,
        }
        
        return jsonify(driver_data)
    
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
                'nombre': escuderia.nombre,
                'campeonatos_mundiales': escuderia.campeonatos_mundiales,
                'lider': escuderia.lider,
                'imagen': escuderia.imagen,
            }
            escuderias_data.append(escuderia_data)
        return jsonify({'escuderias': escuderias_data})
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500
    
@app.route('/escuderias/<int:id_escuderia>', methods=['GET'])
def get_team(id_escuderia):
    try:
        escuderia = Escuderia.query.get(id_escuderia)

        if not escuderia:
            return jsonify({'message': 'Escudería no encontrada'}), 404

        team_data = {
            'id': escuderia.id_escuderia,
            'nombre': escuderia.nombre,
            'campeonatos_mundiales': escuderia.campeonatos_mundiales,
            'lider': escuderia.lider,
            'imagen': escuderia.imagen,
        }
        
        return jsonify(team_data)
    
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500
    
@app.route('/circuitos', methods=['GET'])
def get_circuits():
    try:
        circuitos = Circuito.query.all()
        circuitos_data = []
        for circuito in circuitos:
            circuito_data = {
                'id': circuito.id_circuito,
                'NombreCircuito': circuito.nombre,
                'Pais': circuito.ciudad,
                'Distancia': circuito.distancia,
                'Fecha': circuito.fecha, 
            }
            circuitos_data.append(circuito_data)
        return jsonify({'circuitos': circuitos_data})  
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500
    
@app.route('/fechas/<fecha>', methods=['GET'])
def get_fechas(fecha):
    try:
        fechas = db.session.query(Carrera, Circuito).join(Circuito, Carrera.id_circuito == Circuito.id_circuito).filter(Carrera.fecha == fecha).distinct(Carrera.id_circuito).all()
        fechas_data = []
        for fecha, circuito in fechas:
            print(fecha)
            fecha_data = {
                'id': fecha.id_circuito,
                'nombre': circuito.nombre,
                'ciudad': circuito.ciudad,
                'distancia': circuito.distancia,
                #'Fecha': circuito.date.strftime('%Y-%m-%d'), 
            }
            fechas_data.append(fecha_data)
        return jsonify({'fechas': fechas_data})  
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500
    

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.run(host='localhost', port=5000, debug=True)
