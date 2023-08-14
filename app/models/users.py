import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

def get_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="intregradora"
    )
    return mydb

@app.route('/')
def registro_usuarios():
    return render_template('templates/usuarios/registro_usuarios.html') 

@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        id = request.form['id']
        rol = request.form['rol']
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        contraseña = request.form['contraseña']

        # Crear una conexión a la base de datos
        mydb = get_connection()
        cursor = mydb.cursor()

        # Insertar el usuario en la tabla
        sql = "INSERT INTO usuarios (id, rol, nombre, apellido_paterno, apellido_materno, contraseña) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (id, rol, nombre, apellido_paterno, apellido_materno, contraseña)
        cursor.execute(sql, val)
        mydb.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('templates/usuarios/registro_usuarios.html', mensaje='Usuario registrado exitosamente')
    else:
        return 'Método no permitido'

if __name__ == '__main__':
    app.run(debug=True)