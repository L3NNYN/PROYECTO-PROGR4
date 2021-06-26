var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

//Solo se llama en iniciar sesion
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        data: {
            form:{
                nombre:'',
                password:''
            },
        },
        mounted() {
        }, methods: { //Aquí van las funciones VUE 
        }
    });
}