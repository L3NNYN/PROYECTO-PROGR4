var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            productos:[]
        },
        mounted() {
            this.getData(); // Carga los datos desde el inicio
        }, methods: { //Aquí van las funciones VUE 
            getData(){
                axios.get(apiURL('carrito_api')).then((response) => {
                    this.productos = response.data;
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}