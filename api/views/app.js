window.onload = function () {
    var vm = new Vue({
        el: '#app',
        data: {
            form:{
                nombre:'',
                password:''
            },
            // registro
            form2: {
                nombre: '',
                nombre:'',
                password:'',
                cedula:'',
                usuario: '',
                pais: '',
                direccion: '',
                email:'',
                tipo: ''
            },
            paises: [
                {value:1, text:'Nana1,'},
                {value:2, text:'Nana'}
            ],
            // tienda
            imgProps: {
                blank: true, blankColor: '#777', width: 150, height: 150, class: 'mt-2',
            },
            tienda: {
                puntaje: '12',
            }
            
        },
        mounted() {
            // this.getData(); // Carga los datos desde el inicio (se creará más adelante) 
        }, methods: { //Aquí van las funciones VUE 
            login(){
                
            },
            signup(){

            },
            puntajetienda(){

            }
        }
    });
}