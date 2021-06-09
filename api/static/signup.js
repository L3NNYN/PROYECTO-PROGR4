var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

window.onload = function () {
    var vm = new Vue({
        el: '#app',
        data: {
            // registro
            form: {
                nombre: '',
                // cedula:'',
                // telefono: '',
                // password:'',
                // usuario: '',
                // pais: '',
                // direccion: '',
                // email:'',
                // tipo: ''
            },
            paises:[],
        },
        mounted() {
            // this.getData(); // Carga los datos desde el inicio (se creará más adelante) 
            this.getDataSignUp();
        }, methods: { //Aquí van las funciones VUE 
            getDataSignUp(){
                axios.get(apiURL('paises'))
                .then((response) => {
                    this.paises = response.data;
                }).catch(error => { alertify.error(error); });
            },
            login(){
                
            },
            signup(){
                axios.post(apiURL('signup'), JSON.stringify(this.form))
                .then((response) => {
                }).catch(error => { alertify.error(error); });
            },
            save(evt){      
                evt.preventDefault()
                    // if(this.form.nombre != '' && this.form.telefono != '' && this.form.email != '' && this.form.direccion && this.form.pais && this.form.foto && this.form.tipo && this.form.usuario && this.form.password){
                        this.signup();
                    // }
            },
            puntajetienda(){

            }
        }
    });
}