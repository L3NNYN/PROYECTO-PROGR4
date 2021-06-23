var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            select:'',
            tipo: '',
            wenas: 'JEJE',
            
            suscripciones:{
                tiendas:[],
                productos:[]
            },
            reportes:{
                facturas:[],
                ventas: [],
                compras: [],
                ventas: []
            },
            fields:{
                facturas:['descripcion', 'tiempo envio', 'costo envio', 'cantidad', 'precio'],
                suscripciones:{
                    tiendas:['nombre', 'email'],
                    productos:['descripcion', 'categoria', 'precio', 'tienda']
                }
            }

        },
        mounted() {
            
        }, methods: { //Aquí van las funciones VUE 
            getData(){

            },
            getFacturas(){
                axios.get(apiURL('reporte_facturas_api')).then((response) => {
                    this.reportes.facturas = response.data;
                    console.log(response.data);
                }).catch(error => { alertify.error(error); });
            },
            getVentas(){

            },
            getSuscripciones(){
                axios.get(apiURL('reporte_suscripciones_api')).then((response) => {
                    var aux = this.suscripciones;
                    aux.productos = response.data[0];
                    aux.tiendas  = response.data[1];
                }).catch(error => { alertify.error(error); });
            },
            clean(){
                this.reportes.facturas = [];
                this.reportes.ventas = [];
                this.reportes.suscripciones = [];
                this.reportes.compras = [];
                this.reportes.ventas = [];
            },
            seleccion(){
                switch (this.tipo) {
                    case 'C':
                        break;
                    case 'F':
                        this.getFacturas();
                        break;
                    case 'S':
                        this.getSuscripciones();
                        break;
                    case 'P':
                        break;
                    case 'V':
                        this.getVentas();
                        break;
                    default:
                        alertify.error('No un tipo de reporte seleccionado');
                        break;
                }
            },
            mostrar(){
                if(this.select == '') {
                    alertify.error("Seleciona un tipo de reporte");
                } else {
                    this.tipo = this.select;
                    this.clean();
                    this.seleccion();
                }
            }

        }
    });
}