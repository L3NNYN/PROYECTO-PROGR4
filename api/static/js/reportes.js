var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

var fechaInicio;
var fechaFin;

window.onload = function () {
    var myChart = null;
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            id:'',
            select:'',
            tipo:'',
            ofertas:{
                precioMenor:'',
                categoria:'',
            },
            fechaInicio:'',
            fechaFin:'',
            fechas:{
            },
            precioMenor:'',
            suscripciones:{
                tiendas:[],
                productos:[]
            },
            reportes:{
                facturas:[],
                ventas: [],
                compras: [],
                ofertas: []
            },
            categorias:[],
            fields:{
                compras:['descripcion', 'cantidad', 'precio','total'],
                facturas:['descripcion', 'tiempo envio', 'costo envio', 'cantidad', 'precio'],
                suscripciones:{
                    tiendas:['nombre', 'email'],
                    productos:['descripcion', 'precio','categoria', 'tienda']
                },
                ofertas:['descripcion', 'categoria', 'precio', 'publicacion'],
                ventas:['descripcion', 'stock', 'publicacion', 'precio', 'tiempo envio', 'costo envio', 'categoria']
            }

        },
        mounted() {
            this.id = document.getElementById('id').value;
            // this.visibilityFechas();
            this.getCategorias();
        }, methods: { //Aquí van las funciones VUE 
            getCategorias(){
                axios.get(apiURL('categorias_productos_api'))
                .then((response) => {
                    this.categorias = response.data;
                    this.ofertas.categoria = this.categorias;
                }).catch(error => { alertify.error(error); });
            },
            getFacturas(){
                axios.get(apiURL('reporte_facturas_api')).then((response) => {
                    this.reportes.facturas = response.data;
                }).catch(error => { alertify.error(error); });
            },
            getVentas(){
                axios.get(apiURL('reporte_ventas_api')).then((response) => {
                    this.reportes.ventas = response.data;
                }).catch(error => { alertify.error(error); });
            },
            getCompras(){
                axios.post(apiURL('reporte_compras_api'), JSON.stringify({'fechaInicio':this.fechaInicio, 'fechaFin':this.fechaFin}))
                .then((response) => {
                    this.reportes.compras = response.data;
                    var compras = [];
                    compras = this.reportes.compras;
                    var labels = [];
                    var data= [];
                    if(myChart != null){
                        myChart.destroy();
                    }
                    if(compras != []){
                        compras.forEach((item) =>{
                            labels.push(item['descripcion']);
                            data.push(item['total']);
                        });
                        this.grafico(labels, data);
                    }

                }).catch(error => { alertify.error(error); });
            },
            getSuscripciones(){
                axios.get(apiURL('reporte_suscripciones_api')).then((response) => {
                    var aux = this.suscripciones;
                    aux.productos = response.data[0];
                    aux.tiendas  = response.data[1];
                }).catch(error => { alertify.error(error); });
            },
            getOfertas(){
                var info = {'fechaInicio': this.fechaInicio, 
                            'fechaFin':this.fechaFin, 
                            'precio':this.ofertas.precioMenor, 
                            'categoria':this.ofertas.categoria}
                axios.post(apiURL('reporte_ofertas_api'),JSON.stringify(info)).then((response) => {
                    this.reportes.ofertas = response.data;
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
                        this.getCompras();
                        break;
                    case 'O':
                        this.getOfertas();
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
                }else {
                    this.tipo = this.select;
                    this.clean();
                    this.seleccion();
                }
            },
            grafico(labels, dataset){
                var ctx = document.getElementById('myChart').getContext('2d');
                
                var data = {
                    labels: [
                    'Red',
                    'Blue',
                    'Yellow'
                    ],
                    // labels:labels,
                    datasets: [{
                    label: 'My First Dataset',
                    data: [300, 50, 100],
                    // data: dataset,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                    ],
                    hoverOffset: 4
                    }]
                };

                myChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: data,
                });
            }

        }
});

}