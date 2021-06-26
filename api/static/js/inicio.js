var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

//Ventana de inicio
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
            this.getData(); //Carga los datos
        }, methods: { 
            getData(){
                this.getTiendas(this.filtro);
                this.getProductos(this.filtro);
                this.getMasVendidos(this.filtro);
            },
            //Obtiene todas las tiendas, filtradas o no
            getTiendas(filter){
                var url;
                if(filter){
                    url = apiURL('todo_tiendas_api/'+ filter);
                } else {
                    url = apiURL('todo_tiendas_api');
                }
                axios.get(url).then((response) => {
                    this.tiendas = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Obtiene tods los prodcutos filtrados filtrados o no
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
            //Obtiene los productos mas vendidos filtrados filtrados o no
            getMasVendidos(filter){
                var url;
                if(filter){
                    url = apiURL('mas_vendidos_api/'+ filter);
                } else {
                    url = apiURL('mas_vendidos_api');
                }
                axios.get(url)
                .then((response) => {
                    this.masVendidos = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Boton buscar
            filtrar(){
               this.getProductos(this.filtro);
               this.getTiendas(this.filtro);
               this.getMasVendidos(this.filtro);
            },
            //Agregar al carrito
            agregarCarrito(id, tienda_id){
                axios.post(apiURL('add_carrito_api'), JSON.stringify({'id':id, 'tienda_id': tienda_id}))
                .then((response) => {
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            }
        }
    });
}