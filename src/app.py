from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
'''Marshmallow: me permite definir un esquema con el cual interactuar.
'''
from flask_marshmallow import Marshmallow
import json

app = Flask(__name__)
'''Se define en donde está la base de datos con el recurso "SQL_ALCHEMY_DATABASE_URI"
    Se define el tipo de base de datos mysql y el DRIVER que se va a utilizar "pymysql"
    Luego se coloca el usuario, la contraseña, sitio en donde está la base de datos y 
    el nombre de la base de datos.
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://userAPI:passUserAPI2022@localhost/api_rest'

'''Se agrega una propiedad llamada "SQLALCHEMY_TRACK_MODIFICATIONS" es una configuración
    por defecto para no generar un WARNING o una advertencia al ejecutar el programa.
'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


'''Se le pasa la configuración de la base de datos al ORM (SQLAlchemy)
    Cuando se ejecuta me devuelve una instancia de la base de datos 
    la cual se guarda en la variable "db", esta variable es la que permitirá
    interactuar con la base de datos.
'''
db = SQLAlchemy(app)
ma = Marshmallow(app)


'''Al ejecutar la API se presento un error con el texto
    "raise RuntimeError(unbound_message) from None RuntimeError: Working outside of application context."
    Al buscar la solución en stackoverFlow estaba la linea "app.app_context().push()"
    con lo cual me permitio la ejecución.
'''
app.app_context().push()

'''Se define lo que se va a guardar en la base de datos, para estos
    se define una clase que hereda un modelo que viene desde la base de datos.
    Ya dentro de la clase se define lo que se va a guardar en la base de datos, por ejemplo:
        Nombre, fecha de creacion, autor, etc.
    Con la clase "Task" se genera la definición de la tabla que se creará en la base de datos
    El ORM crea la tabla por nosotros.
'''


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    '''Definir el constructor de la clase, con esto generamos el modelo de datos
        de la base de datos con la que se va a estar interactuando.
    '''

    def __init__(self, title, description):
        self.title = title
        self.description = description


'''Lo que se hizo con clase "Task" fue definir el modelo, para poderlo crear es necesario
    utilizar un método de la instancia de "db" llamado "create_all", este método lee todas
    nuestras clases y apartir de estas empieza a crear tablas.
'''
db.create_all()

'''Luego de crear las tablas, se crea un esquema para interactuar fácilmente con los modelo de datos o
    tablas.
    Se crea una clase que heredará el "Schema" desde la instancia de "ma"
'''


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')


'''Luego de crear la clase de "Schema" se debe instanciar para poderla utilizar.
    Cuando se vaya a crear una sola tarea solo interactuo con la instancia task_schema.
'''
task_schema = TaskSchema()
'''En caso de trabajar con muchas tareas(app de tareas) se utiliza una instancia que se
    me permite ontener multiples datos que cumplan con los valores de la clase TaskSchema.
'''
tasks_schema = TaskSchema(many=True)


@app.route('/', methods=['GET'])
def home():
    json = {"message": "Server running..."}
    return jsonify(json)


'''Con la ruta "/tasks" se realiza la petición "POST" para poder recibir
    los datos que envía el cliente.
    Los datos se guardan en variables, luego creo una tarea con la clase
    "Task", se crea un esquema que se guarda en una variable y 
    luego se guarda en la base de datos y se finaliza la operación.
    Por ultimo se responde al cliente con la información de la tarea poara que vea lo que ha creado.

'''


@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']

    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)


'''Con la misma ruta "/tasks" se realiza la petición "GET" para
    poder consultar toda la información de la base de datos.
    Con la misma clase "Task" se genera la consulta de la información.

'''


@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)


'''Se implementa la ruta que me permitirá consultar
    una sola tarea desde el cliente, ingresandole el ID de la tarea
    me retorna la información de dicha tarea.
'''


@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)


'''Para actualizar la información de una sola tarea
    se crea una nueva ruta que va a recibir el ID de la tarea que quiero actualizar
    y recibe los datos que se van a actualizar.
    Se confirma la transacción con el commit y se retorna la misma tarea ya actualizada.
'''


@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)  # Esta es la tarea que quiero actualizar

    # Estos son los datos que quiero actualizar de la tarea.
    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)

'''Se crea la ruta para eliminar de a una tarea con base en el ID ingresado.
'''
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
