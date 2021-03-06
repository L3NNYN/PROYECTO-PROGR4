var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            productos:[],
            direcciones_envio:[],
            fields:['descripcion', 'precio', 'categoria', 'tiempo envio', 'costo envio', 'tienda', 'remover'],
            metodos_pago: [],
            direcciones_envio:[],
            form:{
                metodo_pago:'',
                direccion_envio:'',
                monto: 0,
                saldo_tarjeta:'',
            },
            cvv:'',
        },
        mounted() {
            this.getData(); // Carga los datos desde el inicio
        }, methods: { //Aquí van las funciones VUE 
            getData(){
                this.getDirecciones();
                this.getMetodosPago();
                this.getProductos();
            },
            getProductos(){
                //Obtiene prodcutos en el carrito
                axios.get(apiURL('carrito_api')).then((response) => {
                    this.productos = response.data;
                    this.calcularMonto();
                }).catch(error => { alertify.error(error); });
            },
            calcularMonto(){
                this.form.monto = 0;
                this.productos.forEach((item) =>{
                    this.form.monto += (item['costo envio'] + item['precio']);
                });
            },
            getDirecciones(){
                //Obtener direcciones de envio
                axios.get(apiURL('direcciones_envio_api'))
                .then((response) => {
                    var direcciones = response.data;
                    direcciones.forEach((item) =>{
                        this.direcciones_envio.push({'value': item['id'], 'text': item['casillero'] + ', ' + item['provincia'] +', '+ item['pais']});
                    });
                }).catch(error => { alertify.error(error); });
            },
            getMetodosPago(){
                //Obetener metodos de pago
                axios.get(apiURL('metodos_pago_api'))
                .then((response) => {
                    var tarjetas = response.data;
                    tarjetas.forEach((item)=>{
                        this.metodos_pago.push({'value': item['id'], 'text': item['propietario'] +', '+ item['numero'] + ', $'+ item['saldo']});
                    }) 
                }).catch(error => { alertify.error(error); });
            },
            //Copmpleta el pago actualizando el carrito
            completarPago(){
                axios.post(apiURL('carrito_api'), JSON.stringify(this.form))
                .then((response) => {
                    this.getProductos();
                    //Rebaja el monto en el metodo de pago
                    this.actualizarMetodoPago();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Valida el monto y su saldo
            validarMetodoPago(){
                axios.post(apiURL('validar_monto_api'), JSON.stringify({'metodo_pago':this.form.metodo_pago, 'monto':this.form.monto }))
                .then((response) => {
                    if(response.data == 'T'){
                        this.completarPago();
                    } else {
                        alertify.error('Fondos insuficientes.');
                    }
                }).catch(error => { alertify.error(error); });
            },
            //REbaja el monto de pago
            actualizarMetodoPago(){
                axios.put(apiURL('update_monto_api'), JSON.stringify({'metodo_pago':this.form.metodo_pago, 'monto': this.form.monto}))
                .then((response) => {
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Valida que el CVV sea correcto
            validar(){
                if(this.cvv != '' && this.metodo_pago != ''){
                    axios.post(apiURL('validar_cvv_api'), JSON.stringify({'cvv': this.cvv, 'metodo_pago': this.form.metodo_pago}))
                    .then((response) => {
                        if(response.data['valido'] == 'T'){
                            this.validarMetodoPago();
                        } else {
                            alertify.error('CVV incorrecto.');
                        }
                    }).catch(error => { alertify.error(error); });
                } else {
                    alertify.error('Selecciona un metodo de pago.');
                    return;
                }
            },
            reset(){
                this.cvv = '';
            },
            //Elimina productos del carrito
            removerCarrito(id, tienda_id){
                axios.post(apiURL('remover_carrito_api'), JSON.stringify({'id': id, 'tienda_id': tienda_id})).then((response) => {
                    this.getProductos();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}