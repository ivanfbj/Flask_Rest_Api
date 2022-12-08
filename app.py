from flask import Flask
from products import products

app = Flask(__name__)

# Crear ruta de prueba para validar el funcionamiento del servidor para}
# Cuando el navegador realice la petición a la ruta /ping va a dar la respuesta del return
# De esta manera se puede testear que el servidor este respondiento con algo al navegador.
@app.route('/ping')
def pingt():
    return 'Pong!'

if __name__ == '__main__':
    app.run(debug=True, port=4000)