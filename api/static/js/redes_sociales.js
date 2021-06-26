var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

//Redes sociales
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        data: {
            redes_sociales:[],
            fields: ['descripcion', 'actions'],
            form:{
                id:'',
                descripcion:''
            }
        },
        mounted() {
            this.getData(); 
        }, methods: { 
            //Obtiene las redes sociales
            getData(){
                axios.get(apiURL('redes_sociales_api')).then((response) => {
                    this.redes_sociales = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Nueva red
            insertForm(){
                this.form.id = ''; 
                this.form.descripcion = '';
            },
            //Guarda red
            save(){
                if (this.form.descripcion != ''){
                    if (this.form.id == ''){
                        axios.post(apiURL('redes_sociales_api'), JSON.stringify(this.form)).then((response) => {
                            alertify.success(response.data);
                            this.$refs.modal.hide();
                            this.getData();
                        }).catch(error => { alertify.error(error); });
                    } else {
                        axios.put(apiURL('redes_sociales_api'), JSON.stringify(this.form)).then((response) => {
                            alertify.success(response.data);
                            this.$refs.modal.hide();
                            this.getData();
                        }).catch(error => { alertify.error(error); });
                    }
                } else { 
                    return;
                }
            },
            //Editar la red
            editForm(id, descripcion){
                this.form.id = id;
                this.form.descripcion = descripcion;
            },
            //Borrar red social
            deleteData(id){
                axios.delete(apiURL('redes_sociales_api/' + id)).then((response) => {
                    this.getData();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Reinciiar el modal
            reset(){
                this.form.id = ''; 
                this.form.descripcion = '';
            }
        }
    });
}