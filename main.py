from flask import Flask, request, redirect,  render_template
import pymongo
import pymongo.errors
import os
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

#Crear objeto de tipo flask
app = Flask('__name__')

# Crear configuracion de carpeta donde se van a guardar la imagenes
app.config['UPLOAD_FOLDER'] = './static/img'

# Crear el objeto que se conecta a la base de datos
miConexion = pymongo.MongoClient('mongodb://localhost:27017')

# Crear un objeto que representa la base de datos de mongo
base_datos = miConexion['TIENDA']

# Crear un objeto que representa la coleccion de la base de datos
productos = base_datos['productos']

@app.route('/')
def home():
    try:
        mensaje = None
        lista_productos = list(productos.find())  # Convertimos el cursor a lista
        for p in lista_productos:
            print(p)
        if not lista_productos:
            mensaje = 'No hay productos'
        else:
            mensaje = 'Productos listados con éxito'
            
    except pymongo.errors as error:
        mensaje = str(error)
        
    return render_template('index.html', productos = lista_productos, mensaje = mensaje)

@app.route("/agregarProducto", methods=['POST', 'GET'])
def agregar():
    mensaje = ''
    producto = None
    if(request.method == 'POST'):
        try:
            codigo = int(request.form['txtCodigo'])
            nombre = request.form['txtNombre']
            precio = int(request.form['txtPrecio'])
            categoria = request.form['cbCategoria']
            foto = request.files['fileFoto']
            nombreArchivo = secure_filename(foto.filename)
            listaNombreArchivo = nombreArchivo.rsplit(".", 1)
            extension = listaNombreArchivo[1].lower()
            # Crear nombre de la foto utilizando el código del producto
            nombreFoto = f"{codigo}.{extension}"
            producto = {
                "codigo": codigo, 
                "nombre": nombre,
                "precio": precio,
                "categoria": categoria, 
                "foto": nombreFoto
            }
            # Verificar si el producto ya existe por su código
            existe = existeProducto(codigo)
            if not existe:
                resultado = productos.insert_one(producto)
                if (resultado.acknowledged):
                    mensaje = "Producto Agregado Correctamente"
                    
                    # Guardar la foto del producto en la ruta
                    foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
                    return redirect('/')
                else:
                    mensaje = "Problemas al agregar el producto."
            else:
                mensaje = "El producto ya existe."

        except pymongo.errors.PyMongoError as error:
            mensaje = f"Error en la base de datos: {str(error)}"
        
    return render_template('frmAgregarProducto.html', mensaje = mensaje, producto = producto)

def existeProducto(codigo):
    try:
        consulta = {"codigo": codigo}
        producto = productos.find_one(consulta)
        if(producto is not None):
            return True
        else:
            return False
    except pymongo.errors as error:
        print(error)
        return False

@app.route('/consultar/<string:id>', methods=['GET'])
def consultar(id):
    if(request.method == 'GET'):
        try:
            id = ObjectId(id)
            consulta = {"_id": id}
            producto = productos.find_one(consulta)
            return render_template('frmActualizarProducto.html', producto = producto)
        except pymongo.errors.PyMongoError as error:
            mensaje = f"Error en la base de datos: {str(error)}"
            return redirect('/')
    

if __name__ == '__main__':
    app.run(port = 5000, debug = True)