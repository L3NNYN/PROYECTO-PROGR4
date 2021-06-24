var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
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
            this.getData(); // Carga los datos desde el inicio (se creará más adelante) 
        }, methods: { //Aquí van las funciones VUE 
            getData(){
                axios.get(apiURL('categorias_productos_api'))
                .then((response) => {
                    this.categorias = response.data;
                }).catch(error => { alertify.error(error); });
            },
            insertForm(){
                this.formTitle = "Agregar categoria del producto"
            },
            add(){
                axios.post(apiURL('categorias_productos_api'), JSON.stringify(this.form2))
                .then((response) => {
                    this.getData();
                }).catch(error => { alertify.error(error); });
            },
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