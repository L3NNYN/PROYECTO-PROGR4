var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

window.onload = function () {
    var vm = new Vue({
        el: '#app',
        data: {
            form:{
                nombre:'',
                password:''
            },
            // // registro
            // formSignup: {
            //     nombre: '',
            //     nombre:'',
            //     password:'',
            //     cedula:'',
            //     usuario: '',
            //     pais: '',
            //     direccion: '',
            //     email:'',
            //     tipo: ''
            // },
            // paises: [
            //     {value:1, text:'Nana1,'},
            //     {value:2, text:'Nana'}
            // ],
            // // tienda
            // imgProps: {
            //     blank: true, blankColor: '#777', width: 150, height: 150, class: 'mt-2',
            // },
            // tienda: {
            //     puntaje: '12',
            //     value:'4',
            //     search:''
            // },
            // fields:['Nombre', 'Numero', 'CVV', 'F.Vencimiento', 'Saldo'],
            // metodos_pago:{
            //     id: '',
            //     propietario: '',
            //     numero: '',
            //     cvv:'',
            //     fecha:'',
            //     saldo: ''
            // }
            
        },
        mounted() {
            // this.getData(); // Carga los datos desde el inicio (se creará más adelante) 
        }, methods: { //Aquí van las funciones VUE 
            login(){
                
            },
            signup(){
                
            },
            validarSignup(){      
                if(this.form2){

                }
            },
            puntajetienda(){

            },
            

            editForm(id, propietario, numero, cvv, fechaVencimiento, saldo){

            },
            deleteData(id){

            },
        }
    });
}