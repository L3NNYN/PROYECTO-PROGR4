var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
//Mantenimiento de notificaiones
window.onload = function () {
    var xm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            notificaciones: [],
            fields:['descripcion', 'precio'],
        },
        mounted() {
            this.getData();  //Obitene notifiaciones
        }, methods: { 
            //Las obtiene
            getData(){
                axios.get(apiURL('notificaciones_api'))
                .then((response) => {
                    this.notificaciones = response.data;
                    console.log(this.notificaciones);
                }).catch(error => { alertify.error(error); });
            },
            //Guarda al darle visto
            save(){
                axios.delete(apiURL('notificaciones_api'))
                .then((response) => {
                    this.getData();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}