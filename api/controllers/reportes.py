from flask import jsonify, request, render_template, redirect, session, flash
from init import app
from init import mysql

#Devuelve la pagina de reportes
@app.route('/reportes')
def reportes():
    try:
        cur = mysql.connect().cursor()
        if 'usuario' in session:
            return render_template('views/reportes.html')
        else:
            return redirect('/login')
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()

@app.route('/reporte_ventas_api')
def ventas():
    try:
        if 'usuario' in session and session['tipo_usuario'] == 'T':
            cur = mysql.connect().cursor()
            
            _json = request.get_json(force=True)
            _id = session['tienda_id']
            _fecha1 = _json['fecha_inicio']
            _fecha2 = _json['fecha_fin']

            data = []
            query = "SELECT DISTINCT p.id_prod, p.descripcion, SUM(t.cantidad), SUM(c.total) FROM productos t LEFT JOIN tbl_productos p ON p.id_prod = t.id_prod LEFT JOIN tbl_compras c ON c.id_comp = t.id_comp WHERE p.usr_id = %s AND c.fecha BETWEEN %s AND %s GROUP BY p.id_prod"
            values = (_id, _fecha1, _fecha2)
            cur.execute(query, values)
            rows = cur.fetchall()
            for row in rows:
                data.append({'id': row[0], 'descripcion': row[1],'cantidad': row[2], 'total': row[3]})

            return jsonify(data)
        else:
            return jsonify('Debes registrarte como tienda')
        
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()

@app.route('/reporte_facturas_api')
def facturas():
    try:
        cur = mysql.connect().cursor()

        facturas = []
        data = {}
        cur.execute("SELECT t.id_comp, DATE_FORMAT(t.fecha, %s), t.total, p.nombrepropietario, p.numero, u.nombre, d.numcasillero, d.provincia FROM tbl_compras t LEFT JOIN tbl_metodosdepago p ON t.id_pago = p.id_pago LEFT JOIN tbl_usuarios u ON u.id_usr = t.id_tienda LEFT JOIN tbl_direccionesdeenvio d ON d.id_dire = d.id_dire WHERE t.id_comprador = %s", ("%d %M %Y",session['id'],))
        rows = cur.fetchall()
        for row in rows:
            data = {'id': row[0], 'fecha':row[1], 'total':row[2], 'metodopago':{'propietario': row[3], 'numero': row[4]}, 'tienda': row[5], 'direccionenvio': {'casillero':row[6], 'provincia':row[7]}, 'productos':[]}
            
            cur.execute("SELECT p.descripcion, p.tiempoenvio, p.costoenvio, t.cantidad, p.precio FROM productos t LEFT JOIN tbl_productos p ON p.id_prod = t.id_prod WHERE t.id_comp = %s", (data['id'], ))
            prods = cur.fetchall()
            for prod in prods:
                data['productos'].append({'descripcion': prod[0], 'tiempo envio': prod[1], 'costo envio':prod[2], 'cantidad':prod[3], 'precio':prod[4]})
            
            facturas.append(data)

        return jsonify(facturas)
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()

@app.route('/reporte_suscripciones_api')
def suscripciones():
    try:
        cur = mysql.connect().cursor()
        data = []
        tiendas = []
        cur.execute("SELECT u.id_usr, u.nombre, u.email FROM seguir t LEFT JOIN tbl_usuarios u ON u.id_usr = t.id_tienda WHERE t.id_comprador =%s ", (session['id'],))
        rows = cur.fetchall()
        for row in rows:
            tiendas.append({'id': row[0], 'nombre':row[1], 'email':row[2]})

        productos = []
        cur.execute("SELECT u.descripcion, c.descripcion, u.precio FROM listadeseos t LEFT JOIN tbl_productos u ON u.id_prod = t.id_producto LEFT JOIN tbl_categoriasproductos c ON u.id_categoria = c.id_catp WHERE t.usr_id =%s ", (session['id'],))
        rows = cur.fetchall()
        for row in rows:
            productos.append({'id': row[0], 'nombre':row[1], 'email':row[2]})


        data.append({'productos':productos})
        data.append({'tiendas': tiendas})
        return jsonify(data)

    except Exception as e:
        print(e)
    finally:
        cur.close()
