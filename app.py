from flask import Flask, jsonify
from products import products

app = Flask(__name__)

# Crear ruta de prueba para validar el funcionamiento del servidor para}
# Cuando el navegador realice la petición a la ruta /ping va a dar la respuesta del return
# De esta manera se puede testear que el servidor este respondiento con algo al navegador.
# Lasa rutas funcionan por defecto con la ruta GET en caso de no especificar al atributo "methods"
@app.route('/ping')
def pingt():
    return jsonify({"message":"Servidor activo, se le retorna al navegador un mensaje en formato JSON."})

# Con la ruta "/products" lo que podemos hacer es retornar la lista de productos que tenemos en el archivo products.py
# Se puede retornar directamente la lista o por medio de una propiedad o se puede incluir otra propiedad.py
# Los ejemplo quedan comentareados en la función.
@app.route('/products', methods=['GET'])
def getProducts():
    # return jsonify(products)
    # return jsonify({"products": products})
    return jsonify({"products": products,
                    "message": "Product's List"})

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    print(product_name)
    return 'received'
    

if __name__ == '__main__':
    app.run(debug=True, port=4000)