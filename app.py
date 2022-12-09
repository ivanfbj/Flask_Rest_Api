# jsonify: me permite retornar un diccionario como un objeto JSON.
# request: lo que hace es proporcionarme los datos que me están enviando a traves de peticiones http
from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

# Crear ruta de prueba para validar el funcionamiento del servidor para}
# Cuando el navegador realice la petición a la ruta /ping va a dar la respuesta del return
# De esta manera se puede testear que el servidor este respondiento con algo al navegador.
# Lasa rutas funcionan por defecto con la ruta GET en caso de no especificar al atributo "methods"


@app.route('/ping')
def ping():
    return jsonify({"message": "Servidor activo, se le retorna al navegador un mensaje en formato JSON."})

# Con la ruta "/products" lo que podemos hacer es retornar la lista de productos que tenemos en el archivo products.py
# Se puede retornar directamente la lista o por medio de una propiedad o se puede incluir otra propiedad.py
# Los ejemplo quedan comentareados en la función.


@app.route('/products', methods=['GET'])
def getProducts():
    # return jsonify(products)
    # return jsonify({"products": products})
    return jsonify({"products": products,
                    "message": "Product's List"})

# Dentro de esta ruta se recibe el nombre del producto para poder buscarlo y retornar la información.
# En caso de no encontrar el registro retorna el mensaje de producto no encontrado.


@app.route('/products/<string:product_name>', methods=['GET'])
def getProduct(product_name):
    productsFound = [
        product for product in products if product['name'] == product_name]
    if (len(productsFound) > 0):
        return jsonify({"product": productsFound[0]})
    return jsonify({"message": "Product not found"})

# Ruta para crear nuevos productos, se utiliza el tipo de petición POST.
# Esta funcionalidad deja la nueva información en memoria ya que no se están
# modificando el archivo directamente.


@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message": "Product Added Succesfully",
                    "products": products})


if __name__ == '__main__':
    app.run(debug=True, port=4000)
