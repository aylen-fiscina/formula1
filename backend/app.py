from flask import Flask, request, jsonify
from db.formula1 import db, Drivers

app = Flask(__name__)
port = 5000

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://intro:intro@localhost:5432/formula1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def hello_world():
    return 'Hello !'


@app.route('/pilotos', methods=['GET'])
def get_drivers():
    try:
        pilotos = Drivers.query.all()
        pilotos_data = []
        for drivers in pilotos:
            drivers_data = {
                'id': drivers.id,
                'Nombre': drivers.firstName,
                'Apellido': drivers.lastName,
                'Nacionalidad': drivers.city,
                'Equipo': drivers.team,
                'Podios': drivers.podiums,
                'Campeonatos Mundiales': drivers.world_champions,   
            }
            pilotos_data.append(drivers_data)
        return jsonify({'pilotos': pilotos_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    
if __name__ == '__main__':
    db.init_app(app)  
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")  
    app.run(host='0.0.0.0', debug=True, port=port)
