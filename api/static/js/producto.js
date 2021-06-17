var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            id:'',
            comentarios:[],
            form:{
                descripcion:'',
            },
            'lista_deseos':'',
            'lala':'',
        },
        mounted() {
            this.id = document.getElementById('id_producto').value;
            this.getComentarios(); // Carga los datos desde el inicio (se creará más adelante) 
            this.getListaDeseo(); //Revisa si existe en la lista de deseos
        }, methods: { //Aquí van las funciones VUE 
            getListaDeseo(){
                axios.get(apiURL('lista_deseos_api/' + this.id))
                .then((response) => {
                    this.lista_deseos = response.data;
                }).catch(error => {console.log(error); alertify.error(error); });
            },
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
            getComentarios(){
                axios.get(apiURL('comentarios_api/' + this.id))
                .then((response) => {
                    this.comentarios = response.data;
                }).catch(error => { alertify.error(error); });
            },
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
            agregarCarrito(){
                axios.post(apiURL('add_carrito_api'), JSON.stringify({'id':this.id}))
                .then((response) => {
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}