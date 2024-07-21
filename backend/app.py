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
            'id_escuderia': piloto.id_escuderia,
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

@app.route('/pilotos/<int:id_piloto>', methods=['PUT'])
def edit_driver(id_piloto):
    try:
        data = request.json
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        piloto = Piloto.query.get(id_piloto)
        if not piloto:
            return jsonify({'message': f'Piloto with id {id_piloto} not found'}), 404

        if 'nombre' in data:
            piloto.nombre = data['nombre']
        if 'apellido' in data:
            piloto.apellido = data['apellido']
        if 'ciudad' in data:
            piloto.ciudad = data['ciudad']
        if 'podios' in data:
            piloto.podios = data['podios']
        if 'campeonatos_mundiales' in data:
            piloto.campeonatos_mundiales = data['campeonatos_mundiales']
        if 'numero' in data:
            piloto.numero = data['numero']
        if 'imagen' in data:
            piloto.imagen = data['imagen']
        if 'id_escuderia' in data:
            piloto.id_escuderia = data['id_escuderia']

        db.session.commit()

        return jsonify({
            'success': True,
            'id': piloto.id_piloto,
            'message': f'Piloto with id {id_piloto} successfully updated'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500
@app.route('/pilotos/<int:id_piloto>', methods=['DELETE'])
def eliminar_piloto(id_piloto):
    try:
        piloto = Piloto.query.get(id_piloto)
        if not piloto:
            return jsonify({'success': False, 'message': f'Piloto with id {id_piloto} not found'}), 404
        carreras = Carrera.query.filter_by(id_piloto=id_piloto).all()
        if carreras:
         
         for carrera in carreras:
             db.session.delete(carrera)

        db.session.delete(piloto)
        db.session.commit()

        return jsonify({'success': True, 'message': f'Piloto with id {id_piloto} deleted successfully'}), 200

    except Exception as error:
        print('Error:', error)
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
        
@app.route('/pilotos', methods=['POST'])
def nuevo_piloto():
    try:
        
        data = request.json
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        escuderia= data.get('escuderia')
        ciudad = data.get('ciudad')
        podios = data.get('podios')
        campeonatos_mundiales = data.get('campeonatos_mundiales')
        numero = data.get('numero')
        imagen = data.get('imagen')
        
        nuevo_piloto = Piloto(nombre=nombre,apellido=apellido,ciudad=ciudad,id_escuderia=escuderia,podios=podios,campeonatos_mundiales=campeonatos_mundiales, numero=numero, imagen=imagen)
        db.session.add(nuevo_piloto)
        db.session.commit()
        
    except :
        return jsonify({'message': 'No se pudo crear'}), 500

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
                'nombre_circuito': circuito.nombre,
                'pais': circuito.ciudad,
                'distancia': circuito.distancia,
                'fecha': circuito.fecha, 
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
            fecha_data = {
                'id': fecha.id_circuito,
                'nombre': circuito.nombre,
                'ciudad': circuito.ciudad,
                'distancia': circuito.distancia,
                'fecha': circuito.fecha, 
            }
            fechas_data.append(fecha_data)
        return jsonify({'fechas': fechas_data})  
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}),500
    
@app.route('/fechas/tabla/<fecha>&<id>', methods=['GET'])
def get_tabla(fecha, id):
    try:
        carreras = db.session.query(Carrera, Piloto, Escuderia).join(Piloto, Carrera.id_piloto == Piloto.id_piloto).join(Escuderia, Piloto.id_escuderia == Escuderia.id_escuderia).filter(Carrera.fecha == fecha, Carrera.id_circuito == id).all()
        carrera_data = []
        for race, piloto, escuderia in carreras :
            race_data = {
                'piloto_nombre': piloto.nombre,
                'piloto_apellido': piloto.apellido,
                'posicion': race.pos,
                'puntos': race.puntos,
                'escuderia_imagen': escuderia.imagen,
                'escuderia_nombre': escuderia.nombre,           
            }
            carrera_data.append(race_data)
        return jsonify({'carrera': carrera_data})
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Error interno del servidor'}), 500
    

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=5000, debug=True)
