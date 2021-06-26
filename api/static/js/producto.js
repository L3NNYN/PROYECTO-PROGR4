var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

//datos del produto
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            id:'',
            tienda_id:'',
            comentarios:[],
            form:{
                descripcion:'',
            },
            'lista_deseos':'',
            calificacion:{
                dada:0,
                nueva:0,
            },
            'puntaje':0,
            'lala':'',
        },
        mounted() {
            this.id = document.getElementById('id_producto').value;
            this.tienda_id = document.getElementById('tienda_id').value;
            this.getData();
        }, methods: { 
            getData(){
                this.getComentarios(); //Comentarios del producto
                this.getListaDeseo(); //Revisa si existe en la lista de deseos
                this.getCalificacion();
            },
            //Obtiene estado de la lista de deseo
            getListaDeseo(){
                axios.get(apiURL('lista_deseos_api/' + this.id))
                .then((response) => {
                    this.lista_deseos = response.data;
                }).catch(error => {console.log(error); alertify.error(error); });
            },
            //Actualiza lista de deseo
            actualizarListaDeseos(){
                agregar = '';
                if(this.lista_deseos == 'T'){
                    agregar = 'F';
                } else {
                    agregar = 'T';
                }
                axios.post(apiURL('lista_deseos_api/'+ this.id), JSON.stringify({'agregar': agregar}))
                .then((response) => {
                    // this.lista_deseos = response.data;
                    this.getListaDeseo();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Obtiene comentarios
            getComentarios(){
                axios.get(apiURL('comentarios_api/' + this.id))
                .then((response) => {
                    this.comentarios = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Calificaion del prodcuto
            getCalificacion(){
                axios.get(apiURL('calificacion_producto_api/'+this.id),).then((response) => {
                    var data = response.data;
                    this.calificacion.dada = data[0].dada;
                    this.puntaje = data[1].producto;
                }).catch(error => { alertify.error(error); });
            },
            //Gaurda calificacion del producto
            async saveCalificacion(){
                if(this.calificacion.dada == 0){
                    await axios.post(apiURL('calificacion_producto_api/'+this.id), JSON.stringify({'calificacion': this.calificacion.nueva})).then((response) => {
                        alertify.success(response.data);
                    }).catch(error => { alertify.error(error); });
                } else {
                   await axios.put(apiURL('calificacion_producto_api/'+this.id), JSON.stringify({'calificacion': this.calificacion.nueva})).then((response) => {
                        alertify.success(response.data);
                    }).catch(error => { alertify.error(error); });
                }
                this.getData();
            },
            //Guarda un comentario
            postComentario(){
                if(this.form.descripcion != ''){
                    axios.post(apiURL('comentarios_api/' + this.id), JSON.stringify(this.form))
                    .then((response) => {
                        alertify.success(response.data);
                        this.getComentarios();
                        this.form.descripcion = '';
                    }).catch(error => { alertify.error(error); });
                }
            },
            //Agrega al carrito el producto
            agregarCarrito(){
                axios.post(apiURL('add_carrito_api'), JSON.stringify({'id':this.id, 'tienda_id': this.tienda_id}))
                .then((response) => {
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}