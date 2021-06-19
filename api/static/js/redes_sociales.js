var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
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
            this.getData(); // Carga los datos desde el inicio (se creará más adelante) 
        }, methods: { //Aquí van las funciones VUE 
            getData(){
                axios.get(apiURL('redes_sociales_api')).then((response) => {
                    this.redes_sociales = response.data;
                }).catch(error => { alertify.error(error); });
            },
            insertForm(){
                this.form.id = ''; 
                this.form.descripcion = '';
            },
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
            editForm(id, descripcion){
                this.form.id = id;
                this.form.descripcion = descripcion;
            },
            deleteData(id){
                axios.delete(apiURL('redes_sociales_api/' + id)).then((response) => {
                    this.getData();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            reset(){
                this.form.id = ''; 
                this.form.descripcion = '';
            }
        }
    });
}