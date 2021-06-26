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
            },
            redes_sociales:[],
            lista_deseos:[],
            seguidores:[]
        },
        mounted() {
            this.tienda.id = document.getElementById("id").value;
            this.getData(); //Se cargan los datos iniciales
        }, methods: { 
            getData(){
                this.getProductos();
                this.getSeguimiento();
                this.getCalificacion();
                this.getRedesSociales();
                this.getSeguidores();
                this.getListaDeseos();
            },
            //Productos de la tienda
            getProductos(){
                axios.get(apiURL('tienda_api/'+this.tienda.id)).then((response) => {
                    this.productos = response.data;
                }).catch(error => {
                    console.log(error); alertify.error(error); });
            },
            //Funcion de buscar
            search(){
                if(this.tienda.search != ''){
                    axios.get(apiURL('search_tienda_api/'+this.tienda.search +'/'+this.tienda.id)).then((response) => {
                        this.productos = response.data;
                    }).catch(error => { alertify.error(error); });
                } else {
                    this.getProductos();
                }
            },
            //Se obtiene la calificacion
            getCalificacion(){
                axios.get(apiURL('calificacion_tienda_api/'+this.tienda.id),).then((response) => {
                    var data = response.data;
                    this.calificacion.dada = data[0].dada;
                    this.tienda.puntaje = data[1].tienda;
                }).catch(error => { alertify.error(error); });
            },
            //Se actuliza la calificacion
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
            //Seguidores
            getSeguidores(){
                axios.get(apiURL('get_seguidores_api/'+this.tienda.id)).then((response) => {
                    this.seguidores = response.data;
                }).catch(error => { alertify.error(error); });
            },
            // Los productos que estan en listas de deseos
            getListaDeseos(){
                axios.get(apiURL('productos_listadeseos_api/'+this.tienda.id)).then((response) => {
                    this.lista_deseos = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Redes sociales
            getRedesSociales(){
                axios.get(apiURL('redes_sociales_api/'+this.tienda.id)).then((response) => {
                    this.redes_sociales = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Si eres comprador, api para saber si sigues la tienda
            getSeguimiento(){
                axios.get(apiURL('seguimiento_api/'+this.tienda.id)).then((response) => {
                    this.seguir = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Poder actualizar seguimiento
            actualizarSeguimiento(type){
                axios.post(apiURL('seguimiento_api/'+this.tienda.id), JSON.stringify({'seguir': type})).then((response) => {
                    this.getSeguimiento();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}