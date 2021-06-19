var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            imgProps: {
                blank: true, blankColor: '#777', width: 150, height: 150, class: 'mt-2',
            }, 
            tienda: {
                id:'',
                puntaje: '12',
                value:'4',
                search:''
            },
            masVendidos:[],
            productos:[]
        },
        mounted() {
            this.tienda.id = document.getElementById("id");
            this.getData(); // Carga los datos desde el inicio (se creará más adelante) 
        }, methods: { //Aquí van las funciones VUE 
            getData(){
                this.getProductos();
            },
            getProductos(){
                axios.get(apiURL('tienda_api')).then((response) => {
                    this.productos = response.data[0];
                    // this.masVendidos = response.data.masVendidos;
                    // console.log(response.data);
                    console.log(this.productos);
                }).catch(error => { alertify.error(error); });
            },
            search(){
                axios.get(apiURL('tienda_api'), JSON.stringify({'search': this.search})).then((response) => {
                    this.productos = response.data.productos;
                }).catch(error => { alertify.error(error); });
            },
            puntajetienda(){

            }
        }
    });
}