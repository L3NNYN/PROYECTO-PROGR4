var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
} window.onload = function () {
    var vm = new Vue({ //Implementación de VUE 
        el: '#app', //Elemento div con id=’app’ 
        data: {
            form:{
                usuario:'',
                password:''
            },
            form2:{
                usuario: '',
                password:'',
                tipo:''
            }
        },
        mounted() {
            // this.login()
        }, methods: { //Aquí van las funciones VUE 

            login() {
                axios.post(apiURL('login'), JSON.stringify(this.form))
                .then((response) => {
                    // window.Location.href = '';
                    console.log(response.data);

                }).catch(error => { alertify.error(error); });
            },

            signup(){
                axios.post(apiURL('signup'), JSON.stringify(this.form2))
                .then((response) => {
                    // window.Location.href = '';
                    console.log(response.data);

                }).catch(error => { alertify.error(error); });
            },

            insertData() { // JSON.stringify formatea el vector para ser enviado como JSON 
                axios.post(apiURL("insert_productos"), JSON.stringify(this.form))
                .then((response) => {
                    this.getData(); 
                    this.$refs.modal.hide(); // oculta el formulario/ventana modal 
                    alertify.success(response.data);
                }).catch((error) => { alertify.error(`Ocurrió un problema al insertar. ${error}`); })
            },

            updateData() {
                axios.put(apiURL("update_productos"), JSON.stringify(this.form))
                .then((response) => {
                    this.getData(); this.$refs.modal.hide(); // oculta el formulario/ventana modal 
                    alertify.success(response.data);
                }).catch((error) => { alertify.error(`Ocurrió un problema al actualizar. ${error}`); })
            },

            async insertForm() { 
                var url = apiURL('get_proveedores/');
                await axios.get(url).then((response) => {
                    this.form.proveedores = response.data;
                }).catch(error => { alertify.error(error); });
                this.formTitle = "Agregar Registro"; 
            },

            async editForm(id, codigo, nombre, precio, cantidad, proveedor) {
                this.form.id = id; 
                this.form.codigo = codigo; 
                this.form.nombre = nombre; 
                this.form.precio = precio; 
                this.form.cantidad = cantidad; 
                this.form.proveedor = proveedor;
                
                //Peticion de los proveedores con axios
                var url = apiURL('get_proveedores/');
                await axios.get(url).then((response) => {
                    this.form.proveedores = response.data;
                }).catch(error => { alertify.error(error); });

                this.formTitle = "Editar Registro"; },

            save(evt) {
                evt.preventDefault()
                    if (this.form.codigo != '' && this.form.nombre != '' && this.form.precio != '' && this.form.cantidad != '' && this.form.proveedor != '') { 
                        if (this.form.id != '') { 
                            this.updateData(); 
                        } else { 
                            this.insertData(); 
                        } 
                    } else { return }
            },

            reset() { this.resetData(); this.formTitle = ''; this.getData(); },

            resetData() { this.form.id = ''; this.form.codigo = ''; this.form.nombre = ''; this.form.precio = ''; this.form.cantidad = ''; this.form.proveedor = ''}
        }
    });
}