import mysql.connector
from flask import Flask, render_template, request, redirect, jsonify, session, url_for
import datetime

app = Flask(__name__)
app.config['SECRET_KEY']='My secret key'

def get_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="integradora"
    )
    return mydb


@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        # Crear una conexión a la base de datos
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Consultar la base de datos para verificar el usuario y la contraseña
        query = "SELECT * FROM usuarios  WHERE usuario = %s AND contraseña = %s"
        values = (usuario, contraseña)
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if result is None:
            # Usuario no registrado o contraseña incorrecta uwu
            mensaje = 'Usuario no registrado o contraseña incorrecta'
            cursor.close()
            connection.close()
            return render_template('rol/iniciar_sesion.html', mensaje=mensaje)
        
        rol = result['rol']
        cursor.close()
        connection.close()
        session['user'] = result

        if rol == 'Administrador':
            # Redirigir a la página del administrador
            return redirect('/Usuario_administrador')
        elif rol == 'Empleado':
            # Redirigir a la página del empleado
            return redirect('/Usuario_empleado')
        else:
            # Otro rol no válido
            mensaje = 'Rol no válido'
            return render_template('rol/iniciar_sesion.html', mensaje=mensaje)
    
    return render_template('rol/iniciar_sesion.html')

@app.route('/Usuario_administrador')
def Usuario_administrador():
    if session.get('user')['rol'] == 'Administrador':
        return render_template('rol/usuario-administrador.html')
    else: 
        return redirect(url_for('Usuario_empleado'))

@app.route('/Usuario_empleado')
def Usuario_empleado():
    return render_template('rol/usuario-empleado.html')

#Usuarios

#apartado usuarios
@app.route('/apartados/apartado_usuario_administrador')
def apartado_usuario():
    return render_template('apartados/apartado-usuario-administrador.html')

#editar usuarios

@app.route('/usuarios/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'POST':
        # Lógica para actualizar el usuario en la base de datos
        # Redirigir a la página de consulta de usuarios
        return redirect(url_for('consultar_usuarios'))
    else:
        # Obtener los detalles del usuario desde la base de datos usando su ID
        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        cursor.close()
        mydb.close()
        
        return render_template('usuarios/editar_usuario.html', usuario=usuario)

@app.route('/usuarios/usuario_editado', methods=['POST'])
def actualizar_usuario():
    if request.method == 'POST':
        id = int(request.form['id'])
        rol = request.form['rol']
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        contraseña = request.form['contraseña']

        # Crear una conexión a la base de datos
        mydb = get_connection()
        cursor = mydb.cursor()

        # Actualizar el usuario en la tabla
        sql = "UPDATE usuarios SET rol=%s, nombre=%s, apellido_paterno=%s, apellido_materno=%s, contraseña=%s WHERE id=%s"
        val = (rol, nombre, apellido_paterno, apellido_materno, contraseña, id)
        cursor.execute(sql, val)
        mydb.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('usuarios/Editar_usuario.html', mensaje='Usuario actualizado exitosamente')
    else:
        return 'Método no permitido'
    



#eliminar usuarios
@app.route('/usuarios/eliminar_usuarios')
def eliminar_usuarios():
    return render_template('usuarios/eliminar_usuario.html') 


#regristar usaurios
@app.route('/usuarios/registrar_usuarios')
def registro_usuarios():
    return render_template('usuarios/registro_usuarios.html') 

@app.route('/guardar_usuario', methods=['GET', 'POST'])
def guardar_usuario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        rol = request.form['rol']
        usuario = request.form['usuario']
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        contraseña = request.form['contraseña']

        # Crear una conexión a la base de datos (reemplaza esto con tu propia función get_connection())
        mydb = get_connection()
        cursor = mydb.cursor()

        # Insertar el usuario en la tabla
        sql = "INSERT INTO usuarios (rol, usuario, nombre, apellido_paterno, apellido_materno, contraseña) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (rol, usuario, nombre, apellido_paterno, apellido_materno, contraseña)
        cursor.execute(sql, val)
        mydb.commit()

        # Obtener todos los usuarios de la base de datos
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('usuarios/registro_usuarios.html', usuarios=usuarios, mensaje='Usuario registrado exitosamente')
    else:
        return render_template('usuarios/registro_usuarios.html')  # Mostrar el formulario
    

#consultar usuario
@app.route('/usuarios/consultar_usuarios/', methods=['GET', 'POST'])
def consultar_usuarios():
    if request.method == 'POST':
        # Obtener el ID del usuario
        id = request.form['id']
        accion = request.form['accion']
        mensaje = ''  # Inicializar la variable mensaje

        # Crear una conexión a la base de datos
        mydb = get_connection()
        cursor = mydb.cursor()

        if accion == 'eliminar':
            # Eliminar el usuario de la tabla
            sql = "DELETE FROM usuarios WHERE id=%s"
            val = (id,)
            cursor.execute(sql, val)
            mydb.commit()
            mensaje = 'Usuario eliminado exitosamente'
        elif accion == 'editar':
            # Aquí podrías redirigir a una página de edición con el ID del usuario
            # por ejemplo: return redirect(f'/usuarios/editar_usuario/{id}')
            pass  # Agrega el bloque de código para editar aquí

        # Obtener todos los usuarios de la tabla
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('usuarios/consultar_usuarios.html', usuarios=usuarios, mensaje=mensaje)

    else:
        # Crear una conexión a la base de datos
        mydb = get_connection()
        cursor = mydb.cursor()

        # Obtener todos los usuarios de la tabla
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('usuarios/consultar_usuarios.html', usuarios=usuarios)
    

#vista administradores
@app.route('/usuarios/vista_administradores')
def vista_administradores():
    # Crear una conexión a la base de datos
    mydb = get_connection()
    cursor = mydb.cursor()

    # Obtener los usuarios con rol de "Administrador" desde la vista
    cursor.execute("SELECT * FROM vista_administradores")
    administradores = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    mydb.close()

    return render_template('usuarios/vista_administradores.html', administradores=administradores)

        

#inventario

#apartado inventario
@app.route('/apartados/apartado_inventario_administrador')
def apartado_inventario():
    return render_template('apartados/apartado-inventario-administrador.html')
#regristar producto
@app.route('/producto/regristar_producto')
def regristo_producto():
    return render_template('producto/Regristo_productos.html')

@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        precio = request.form['precio']
        marca = request.form['marca']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        caducidad = request.form['caducidad']

        # Crear una conexión a la base de datos
        mydb = get_connection()
        cursor = mydb.cursor()

        # Insertar el producto en la tabla
        sql = "INSERT INTO productos (nombre, precio, marca, categoria, cantidad, caducidad) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (nombre, precio, marca, categoria, cantidad, caducidad)
        cursor.execute(sql, val)
        mydb.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('producto/Regristo_productos.html', mensaje='Producto registrado exitosamente')
    else:
        return 'Método no permitido'

#consutlar producto
@app.route('/producto/consultar_producto', methods=['GET', 'POST'])
def consultar_producto():
    if request.method == 'POST':
            # Obtener el ID del usuario
            id = request.form['id']
            accion = request.form['accion']
            mensaje = ''  # Inicializar la variable mensaje

            # Crear una conexión a la base de datos
            mydb = get_connection()
            cursor = mydb.cursor()

            if accion == 'eliminar':
                # Eliminar el pruducto de la tabla
                sql = "DELETE FROM productos WHERE id=%s"
                val = (id,)
                cursor.execute(sql, val)
                mydb.commit()
                mensaje = 'Usuario eliminado exitosamente'
            elif accion == 'editar':
                # Aquí podrías redirigir a una página de edición con el ID del usuario
                # por ejemplo: return redirect(f'/usuarios/editar_usuario/{id}')
                pass  # Agrega el bloque de código para editar aquí

            # Obtener todos los usuarios de la tabla
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            # Cerrar la conexión a la base de datos
            cursor.close()
            mydb.close()

            return render_template('producto/consultar_producto.html', productos=productos, mensaje=mensaje)

    else:
            # Crear una conexión a la base de datos
            mydb = get_connection()
            cursor = mydb.cursor()

            # Obtener todos los usuarios de la tabla
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            # Cerrar la conexión a la base de datos
            cursor.close()
            mydb.close()

            return render_template('producto/Consultar_producto.html', productos=productos)





#eliminar producto




#editar producto
@app.route('/producto/editar_producto', methods=['GET'])
def editar_producto():
    return render_template('producto/editar_producto.html')



@app.route('/producto/producto_editado', methods=['POST'])
def actualizar_producto():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        precio = request.form['precio']
        marca = request.form['marca']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        caducidad = request.form['caducidad']

        fecha_actual = datetime.date.today().strftime('%Y-%m-%d')

        # Crear una conexión a la base de datos
        mydb = get_connection()
        cursor = mydb.cursor()

        # Actualizar el usuario en la tabla
        sql = "UPDATE productos SET nombre=%s, precio=%s, marca=%s, categoria=%s, cantidad=%s, caducidad=%s WHERE id=%s"
        val = (nombre, precio, marca, categoria, cantidad, caducidad, id)
        cursor.execute(sql, val)
        mydb.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('producto/editar_producto.html', mensaje='producto actualizado exitosamente')
    else:
        return 'Método no permitido'



#venta

#desea cancelar venta
@app.route('/venta/desea_eliminar_venta')
def desea_editar_venta():
    return render_template('Venta/Desea_cancelar_venta.html')

@app.route('/venta/desea_eliminar_venta_administrador')
def desea_editar_venta_administrador():
    return render_template('Venta/Desea_eliminar_venta_administrador.html')


@app.route('/venta/eliminar_venta')
def eliminar_venta():
    return render_template('Venta/eliminar_venta.html')

@app.route('/venta/eliminar_venta_administrador')
def eliminar_venta_administrador():
    return render_template('Venta/Eliminar_venta.html')


@app.route('/venta/venta_eliminada', methods=['POST'])
def venta_eliminada():
    if request.method == 'POST':
        # Obtener el ID de la venta a eliminar
        id = request.form['id']

        # Crear una conexión a la base de datos
        mydb = get_connection()
        cursor = mydb.cursor()

        # Eliminar el usuario de la tabla
        sql = "DELETE FROM consultas WHERE id=%s"
        val = (id,)
        cursor.execute(sql, val)
        mydb.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('Venta/Eliminar_venta.html', mensaje='Producto eliminado exitosamente')
    else:
        return 'Método no permitido'
    
@app.route('/venta/venta_eliminada_administador', methods=['POST'])
def venta_eliminada_administador():
    if request.method == 'POST':
        # Obtener el ID de la venta a eliminar
        id = request.form['id']

        # Crear una conexión a la base de datos
        mydb = get_connection()
        cursor = mydb.cursor()

        # Eliminar el usuario de la tabla
        sql = "DELETE FROM consultas WHERE id=%s"
        val = (id,)
        cursor.execute(sql, val)
        mydb.commit()

        # Cerrar la conexión a la base de datos
        cursor.close()
        mydb.close()

        return render_template('Venta/Eliminar_venta_administrador.html', mensaje='Producto eliminado exitosamente')
    else:
        return 'Método no permitido'


#venta menu
@app.route('/Venta/Menu_venta')
def Menu_venta():
    return render_template('Venta/Menu_Venta.html')

#hacer Venta
@app.route('/Venta/crear_venta')
def crear_venta():
    # Crear una conexión a la base de datos
    mydb = get_connection()
    cursor = mydb.cursor()

    # Obtener los productos de la base de datos
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    mydb.close()

    return render_template('Venta/Crear_Venta.html', productos=productos)

@app.route('/guardar_venta', methods=['POST'])
def guardar_venta():
    if request.method == 'POST':
        fecha = request.form['fecha']
        producto = request.form['producto']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        total = request.form['total']

        # Crear una conexión a la base de datos
        connection = get_connection()
        cursor = connection.cursor()

        try:
            # Iniciar una transacción
            cursor.execute("START TRANSACTION")

            # Insertar la venta en la tabla sin incluir el campo "id" (será autoincrementado)
            query = "INSERT INTO consultas (fecha, producto, precio, cantidad, total) VALUES ( %s, %s, %s, %s, %s)"
            values = (fecha, producto, precio, cantidad, total)
            cursor.execute(query, values)

            # Confirmar la transacción
            cursor.execute("COMMIT")

            # Actualizar la cantidad en la tabla de productos usando el disparador
            update_trigger_query = "INSERT INTO consultas (producto, cantidad) VALUES (%s, %s)"
            update_trigger_values = (producto, cantidad)
            cursor.execute(update_trigger_query, update_trigger_values)

            return redirect('/Venta/crear_venta')

        except Exception as e:
            # Si ocurre un error, revertir la transacción
            cursor.execute("ROLLBACK")
            return f"Error: {str(e)}"

        finally:
            cursor.close()
            connection.close()

    return 'Método no permitido'

@app.route('/get_nombre_producto', methods=['GET'])
def get_nombre_producto():
    id_producto = request.args.get('id_producto')

    # Crear una conexión a la base de datos
    connection = get_connection()
    cursor = connection.cursor()

    # Obtener el nombre del producto
    query = "SELECT nombre FROM productos WHERE id = %s"
    cursor.execute(query, (id_producto,))
    nombre_producto = cursor.fetchone()

    cursor.close()
    connection.close()

    if nombre_producto:
        return jsonify({'nombre_producto': nombre_producto[0]})
    else:
        return jsonify({'nombre_producto': None})


#hacer ticket
@app.route('/venta/generar_ticket')
def generar_ticket():
    # Obtener los datos de la venta desde la base de datos
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM consultas WHERE fecha = (SELECT MAX(fecha) FROM consultas);"
    cursor.execute(query)
    consultas = cursor.fetchall()

    cursor.close()
    connection.close()

    # Renderizar la plantilla con los datos de la venta como contexto
    return render_template('Venta/Generar_Ticket.html', consulta=consultas[-1])


@app.route('/apartados/corte_de_caja', methods=['GET', 'POST'])
def corte_de_caja():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        fecha_seleccionada = request.form.get('fecha')
        cursor.execute('SELECT SUM(total) AS total_ventas FROM consultas WHERE fecha = %s', (fecha_seleccionada,))
        total_ventas_result = cursor.fetchone()
        total_ventas = total_ventas_result['total_ventas']
    else:
        total_ventas = None

    cursor.execute('SELECT * FROM consultas')
    ventas = cursor.fetchall()

    connection.close()

    return render_template('apartados/apartado-cortecaja-administrador.html', ventas=ventas, total_ventas=total_ventas)


@app.route('/producto/easter_egg')
def easter_egg():

    return render_template('/producto/easter_egg.html')

if __name__ == '__main__':
    app.run(debug=True)