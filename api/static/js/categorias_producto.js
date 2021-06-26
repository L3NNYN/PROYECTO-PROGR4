var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
//Archivo para obtener y mantener las categorias de producto
window.onload = function () {
    var qw = new Vue({
        el: '#app',
        data: {
            form:{
                descripcion: '',
                stock: '',
                precio:'',
                tiempoEnvio:'',
                costoEnvio:'',
                categoria:'',
                fotos:''
            },
            form2:{
                descripcion:''
            },
            categorias:[],
            formTitle:''
        },
        mounted() {
            this.getData(); //Obtiene las categorias de producto
        }, methods: {
            getData(){
                axios.get(apiURL('categorias_productos_api'))
                .then((response) => {
                    this.categorias = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Abre el modal
            insertForm(){
                this.formTitle = "Agregar categoria del producto"
            },
            //Agrega nuevas catgeorias de productos
            add(){
                axios.post(apiURL('categorias_productos_api'), JSON.stringify(this.form2))
                .then((response) => {
                    this.getData();
                }).catch(error => { alertify.error(error); });
            },
            //Las guarda
            save(evt){
                evt.preventDefault()
                if(this.form2.descripcion != ''){
                    this.add();
                }
            },
            reset(){
                this.form2 = '';
                this.formTitle = '';
                this.getData();
            }
        }
    });
}