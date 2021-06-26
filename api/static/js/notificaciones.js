var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
window.onload = function () {
    var xm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            notificaciones: [],
            fields:['descripcion', 'precio'],
        },
        mounted() {
            this.getData(); 
        }, methods: { 
            getData(){
                axios.get(apiURL('notificaciones_api'))
                .then((response) => {
                    this.notificaciones = response.data;
                    console.log(this.notificaciones);
                }).catch(error => { alertify.error(error); });
            },
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