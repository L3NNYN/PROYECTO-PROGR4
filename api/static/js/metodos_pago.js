var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}

window.onload = function () {
    var vm = new Vue({
        el: '#app',
        data: {
            form:{
                id: '',
                propietario:'',
                numero:'',
                cvv:'',
                fecha:'',
                saldo:''
            },
            fields:['propietario', 'numero', 'cvv', 'fecha', 'saldo', 'actions'],
            metodos_pago: [],
            formTitle: ''
        },
        mounted() {
            this.getData();
        }, methods: { //Aquí van las funciones VUE 
            getData(){
                axios.get(apiURL('metodos_pago_api'))
                .then((response) => {
                    this.metodos_pago = response.data;
                }).catch(error => { alertify.error(error); });
            },
            insertData(){
                axios.post(apiURL('metodos_pago_api'), JSON.stringify(this.form))
                .then((response) => {
                    this.getData(); 
                    this.$refs.modal.hide();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            editForm(id, propietario, numero, cvv, fechaVencimiento, saldo){
            },
            deleteData(id){

            },
            insertForm(){
                this.formTitle = "Agregar Metodo de Pago"
            },
            save(evt){
                evt.preventDefault()
                    if(this.form.propietario != '' && this.form.numero != '' && this.form.cvv != '' && this.form.saldo != ''){
                        var name = this.form.propietario;
                        this.form.propietario = name.toUpperCase(); 
                        this.insertData();
                    } else { return}
            },
            reset(){
                this.resetData();
                this.formTitle = '';
                this.getData();
            },
            resetData(){
                this.form.id = '';
                this.form.propietario = '';
                this.form.numero = '';
                this.form.cvv = '';
                this.form.saldo = '';
            }
        }
    });
}