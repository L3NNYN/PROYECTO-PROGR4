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
                puntaje: 0,
                search:''
            },
            seguir: '',
            productos:[],
            calificacion:{
                dada:0,
                nueva:0,
            }
        },
        mounted() {
            this.tienda.id = document.getElementById("id").value;
            this.getData(); // Carga los datos desde el inicio (se creará más adelante) 
        }, methods: { //Aquí van las funciones VUE 
            getData(){
                this.getProductos();
                this.getSeguimiento();
                this.getCalificacion();
            },
            getProductos(){
                axios.get(apiURL('tienda_api/'+this.tienda.id)).then((response) => {
                    this.productos = response.data;
                    // this.masVendidos = response.data.masVendidos;
                    // console.log(response.data);
                }).catch(error => {
                    console.log(error); alertify.error(error); });
            },
            search(){
                axios.get(apiURL('tienda_api/'+this.tienda.id), JSON.stringify({'search': this.search})).then((response) => {
                    this.productos = response.data.productos;
                }).catch(error => { alertify.error(error); });
            },
            getCalificacion(){
                axios.get(apiURL('calificacion_tienda_api/'+this.tienda.id),).then((response) => {
                    var data = response.data;
                    this.calificacion.dada = data[0].dada;
                    this.tienda.puntaje = data[1].tienda;
                }).catch(error => { alertify.error(error); });
            },
            saveCalificacion(){
                if(this.calificacion.dada == 0){
                    axios.post(apiURL('calificacion_tienda_api/'+this.tienda.id), JSON.stringify({'calificacion': this.calificacion.nueva})).then((response) => {
                        alertify.success(response.data);
                    }).catch(error => { alertify.error(error); });
                } else {
                    axios.put(apiURL('calificacion_tienda_api/'+this.tienda.id), JSON.stringify({'calificacion': this.calificacion.nueva})).then((response) => {
                        alertify.success(response.data);
                    }).catch(error => { alertify.error(error); });
                }
                this.getData();
            },
            puntajetienda(){

            },
            getSeguimiento(){
                axios.get(apiURL('seguimiento_api/'+this.tienda.id)).then((response) => {
                    this.seguir = response.data;
                }).catch(error => { alertify.error(error); });
            },
            actualizarSeguimiento(type){
                axios.post(apiURL('seguimiento_api/'+this.tienda.id), JSON.stringify({'seguir': type})).then((response) => {
                    this.getSeguimiento();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}