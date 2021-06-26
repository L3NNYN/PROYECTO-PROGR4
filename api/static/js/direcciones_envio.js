var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

//Mantenimiento de las direcciones de envio
window.onload = function () {
    var vm = new Vue({
        el: '#app',
        data: {
            form:{
                id: '',
                numCasillero:'',
                codPostal:'',
                provincia:'',
                id_pais:'',
            },
            fields:['casillero', 'codPostal', 'provincia', 'pais', 'actions'],
            direcciones_envio: [],
            formTitle: '',
            paises: []
        },
        mounted() {
            this.getData();
        }, methods: { 
            //Obtiene  las direcciones de envio
            getData(){
                axios.get(apiURL('direcciones_envio_api'))
                .then((response) => {
                    this.direcciones_envio = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Ingresa direcciones de envio
            insertData(){
                axios.post(apiURL('direcciones_envio_api'), JSON.stringify(this.form))
                .then((response) => {
                    this.getData(); 
                    this.$refs.modal.hide();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Actualiza direcciones de envio
            updateData(){
                axios.put(apiURL('direcciones_envio_api'), JSON.stringify(this.form))
                .then((response) => {
                    this.getData(); 
                    this.$refs.modal.hide();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Cargaa los datos en la modal
           async editForm(id, numCasillero, codPostal, provincia, pais){
                this.form.id = id;
                this.form.numCasillero = numCasillero;
                this.form.codPostal = codPostal;
                this.form.provincia = provincia;
                this.form.id_pais = pais;
                this.formTitle = "Editar Direccion";

                await axios.get(apiURL('paises_api'))
                .then((response) => {
                    this.paises = response.data;
                }).catch(error => { alertify.error(error); });

            },
            //Borra una direccion de envio
            deleteData(id){
                axios.delete(apiURL('direcciones_envio_api/'+id)).then((response) => {
                    this.getData(); 
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Envia los datos
            async insertForm(){
                await axios.get(apiURL('paises_api'))
                .then((response) => {
                    this.paises = response.data;
                }).catch(error => { alertify.error(error); });
                this.formTitle = "Agregar Direccion de Envio"
            },
            //Gaurdar en modal
            save(evt){
                evt.preventDefault()
                    if(this.form.numCasillero != '' && this.form.codPostal != '' && this.form.provincia != '' && this.form.id_pais != ''){
                        if(this.form.id == ''){
                            this.insertData();
                        } else{
                            this.updateData();
                        }
                    } else { return}
            },
            //Reincia la modal
            reset(){
                this.resetData();
                this.formTitle = '';
                this.getData();
            },
            resetData(){
                this.form.id = '';
                this.form.numCasillero = '';
                this.form.codPostal = '';
                this.form.provincia = '';
                this.form.id_pais = '';
            }
        }
    });
}