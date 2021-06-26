var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

//Este archivo realmente no hace mucho, asi que si puede ignorarlo mejor :)
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        data: {
            // registro
            form: {
                nombre: '',
            },
            paises:[],
        },
        mounted() {
            this.getDataSignUp(); //Se obtienen los paises para poder seleccionar
        }, methods: { 
            getDataSignUp(){
                axios.get(apiURL('paises_api'))
                .then((response) => {
                    this.paises = response.data;
                }).catch(error => { alertify.error(error); });
            },
            signup(){
                axios.post(apiURL('signup'), JSON.stringify(this.form))
                .then((response) => {
                }).catch(error => { alertify.error(error); });
            },
            save(evt){      
                evt.preventDefault()
                        this.signup();
            },
        }
    });
}