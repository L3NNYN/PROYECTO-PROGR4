var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        delimiters: ['[[', ']]'],
        data: {
            search:'',
            tiendas:[],
            masVendidos:[],
            productos:[],
            shoppingItems: [
                { name: 'apple', price: '7' },
                { name: 'orange', price: '12' }
              ],
            filtro:''
        },
        mounted() {
            this.getData(); // Carga los datos desde el inicio (se creará más adelante) 
        }, methods: { //Aquí van las funciones VUE 
            getData(){
                this.getTiendas(this.filtro);
                this.getProductos(this.filtro);
                // this.getMasVendidos();
            },
            getTiendas(filter){
                var url;
                if(filter){
                    url = apiURL('todo_tiendas_api/'+ filter);
                } else {
                    url = apiURL('todo_tiendas_api');
                }
                axios.get(url).then((response) => {
                    this.tiendas = response.data;
                    console.log(this.tiendas);
                }).catch(error => { alertify.error(error); });
            },
            getProductos(filter){
                var url;
                if(filter){
                    url = apiURL('todo_productos_api/'+ filter);
                } else {
                    url = apiURL('todo_productos_api');
                }
                axios.get(url).then((response) => {
                    this.productos = response.data;
                }).catch(error => { alertify.error(error); });
            },
            getMasVendidos(){
                axios.get(apiURL('mas_vendidos_api'))
                .then((response) => {
                    this.masVendidos = response.data;
                }).catch(error => { alertify.error(error); });
            },
            filtrar(){
               this.getProductos(this.filtro);
            },
            agregarCarrito(id){
                axios.post(apiURL('canasta_api'), JSON.stringify({'id':id}))
                .then((response) => {
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}