var BaseApiUrl = "http://localhost:5000/"; //ruta base a la API 
function apiURL(service) { //Función para formar la ruta completa a la API 
    return BaseApiUrl + service;
}
//Mantenimiento de metods de pago
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
            this.getData(); //Datos iniciales
        }, methods: { 
            getData(){
                axios.get(apiURL('metodos_pago_api'))
                .then((response) => {
                    this.metodos_pago = response.data;
                }).catch(error => { alertify.error(error); });
            },
            //Ingresa un metodo de apgo
            insertData(){
                axios.post(apiURL('metodos_pago_api'), JSON.stringify(this.form))
                .then((response) => {
                    this.getData(); 
                    this.$refs.modal.hide();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Actualiza un metodo de pago
            async updateData(){
                await axios.put(apiURL('metodos_pago_api'), JSON.stringify(this.form))
                .then((response) => {
                    this.getData(); 
                    this.$refs.modal.hide();
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Edita un metodo de pago
            editForm(id, propietario, numero, cvv, fechaVencimiento, saldo){
                this.form.id = id;
                this.form.propietario = propietario;
                this.form.numero = numero;
                this.form.cvv = cvv;
                this.form.fecha = fechaVencimiento;
                this.form.saldo = saldo;
                this.formTitle = "Editar Direccion";
            },
            //Borra un metodo de pago
            deleteData(id){
                axios.delete(apiURL('metodos_pago_api/'+id)).then((response) => {
                    this.getData(); 
                    alertify.success(response.data);
                }).catch(error => { alertify.error(error); });
            },
            //Abrea modal
            insertForm(){
                this.formTitle = "Agregar Metodo de Pago"
            },
            //Guarda el formulario 
            save(evt){
                evt.preventDefault()
                    if(this.form.propietario != '' && this.form.numero != '' && this.form.cvv != '' && this.form.saldo != ''){
                        var name = this.form.propietario;
                        this.form.propietario = name.toUpperCase(); 
                        if(this.form.id == ''){
                            this.insertData();
                        } else{
                            this.updateData();
                        }
                    } else { return}
            },
            //Reinicia el modal
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