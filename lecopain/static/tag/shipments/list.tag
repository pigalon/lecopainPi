<search-shipment>
    <div class="form-group">
        <select class="form-control" name="customer_id" id="customer_id" ref="customer_id" style="width: 12rem; display:inline-block" >
            <option value="0" SELECTED>Tous</option>
            <option each="{ customer in customers }" value={customer.id}>{customer.firstname} {customer.lastname}</option>
        </select>
        <input type="text"style="width:200px; display: inline-block;" name="day" ref="day" id="datepicker_day" data-language='fr' class="form-control datepicker-input" />
        <select class="form-control" name="period" id="period" ref="period" style="width: 12rem; display:inline-block">
            <option value="day">Jour</option>
            <option value="week">Semaine</option>
            <option value="month">Mois</option>
            <option value="all">Toutes</option>
        </select>
        <button type="button" ref="search" name="search" id="search" onclick="{load_shipments}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
        <div class="right">
            <a role="button" href="/shipments/new" class="btn btn-primary display:inline-block">Ajouter</a>
        </div>
    </div>
    <table id="shipments_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="20%">Date</th>
                    <th width="30%">Client</th>
                    <th width="15%">Status</th>
                    <th width="10%">Liv.</th>
                    <th width="15%">Actions</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ shipment in shipments }">
            <td>
            
            <table width="100%" class="table table-striped">
                <tr>
                    <td if={shipment.status == 'CREE' && shipment.updated_at == None} width="6%" class="table-primary">{shipment.id}</td>
                    <td if={shipment.status == 'CREE' && shipment.updated_at != None} width="6%" class="table-warning">{shipment.id}</td>
                    <td if={shipment.status == 'ANNULEE'} width="6%" class="table-dark">{shipment.id}</td>
                    <td if={shipment.status == 'TERMINEE'} width="6%" class="table-success">{shipment.id}</td>
                    <td if={shipment.status == 'DEFAUT'} width="6%" class="table-danger">{shipment.id}</td>

                    <td width="20%">{moment(shipment.shipping_dt).format('ddd Do MMMM' )}</td>
                    <td width="30%"><span onclick={ show_shipment(shipment.id) } class="badge badge-primary" style="font-size:14px;"><i class="fas fa-user"></i></span> {shipment.customer_name}</td>
                    <td width="15%">
                        <span if={shipment.shipping_status == 'OUI'} style="color:green" ><i class="fas fa-cart-arrow-down "></i></span>
                        <span if={shipment.shipping_status == 'NON'} style="color:grey" ><i class="fas fa-cart-arrow-down "></i></span>
                        <span if={shipment.payment_status == 'OUI'} style="color:green" ><i class="fas fa-credit-card"></i></span>
                        <span if={shipment.payment_status == 'NON'} style="color:grey" ><i class="fas fa-credit-card"></i></span>
                        <span <span onclick={ show_subscription(shipment.subscription_id) } if={shipment.subscription_id != None} class="badge badge-warning" style="font-size:16px;">Ab.</span>
                    </td>
                    <td if={shipment.status == 'ANNULEE'} width="10%" >0.00 €</td>
                    <td if={shipment.status != 'ANNULEE'} width="10%">
                        {shipment.shipping_price.toFixed(2)} €
                    </td>
                     <td width="15%">
                        <span onclick={ show_shipment(shipment.id) } class="badge badge-primary"><i class="fas fa-eye" style="font-size:18px;"></i></span>
                        <input onclick={ check_shipement } type="checkbox" ref="ids_{shipment.id}" id="ids_{shipment.id}" name="ids_{shipment.id}">
                    </td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ page > 1 } role="button" onclick="{load_shipments_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Livraisons précédentes </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ per_page <= count } role="button" onclick="{load_shipments_next}"  style="color:white" class="btn btn-primary display:inline-block"> Livraisons suivantes <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>
     <div class="right">
        <a role="button" onclick="{ cancel_list }" style="color:white" class="btn btn-primary display:inline-block">Annulation Liste</a>
    </div>

    <br>
    <br>
    <script>
		var self = this
        var per_page = 10
        var page= 1
        var next_url = ''

        this.selected_shipments = []


        moment.locale('fr');

		this.on('mount', function() {
			this.load_shipments()
            
            var ajaxCall_customers = self.load_customers();
			ajaxCall_customers.done(function(data) {
				$(self.refs.customer_id).select2();
			})
            const location  = $('window.location')
            self.refs.day.value = moment().format('DD/MM/YYYY')
		});

        $(function () {
            $("#datepicker_day").datepicker(
                {autoClose: true}
                
            );
        });

		/******************************************/
       	// load shipments list
    	/*******************************************/
		load_shipments(){
            var shipment_url = '/api/shipments/';
            var customer_id = self.refs.customer_id.value;
            var period = self.refs.period.value;

            var day = self.refs.day.value;

            
            
            if (period == undefined){
                period = 'all'
            }

            shipment_url = shipment_url.concat('period/',period,'/');
            shipment_url = shipment_url.concat('date/', day.replaceAll("/",""),'/');
            shipment_url = shipment_url.concat('customers/',customer_id);

			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.update()
                }
            });
		}
        load_shipments_next(){
            var shipment_url = self.next_url;

			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_shipments_previous(){
            var shipment_url = self.previous_url;

			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_customers(){
			var url = '/api/customers/';
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.customers = data['customers']
                    self.update()
                }
            });
		}

        show_shipment(shipment_id){
            return function(e) {
                location = "/shipments/"+shipment_id;
            }
		}
        show_subscription(subscription_id){
            return function(e) {
                location = "/subscriptions/"+subscription_id;
            }
		}
        show_customer(customer_id){
            return function(e) {
                location = "/customers/"+customer_id;
            }
		}

        check_shipement(e){
            if ($('#ids_'+e.item.shipment.id).is(':checked')) {
                this.selected_shipments.push(e.item.shipment.id)
            }
            else{
                for( var i = 0; i < this.selected_shipments.length; i++)
                { 
                    if ( this.selected_shipments[i] === e.item.shipment.id) { 
                        this.selected_shipments.splice(i, 1); 
                    }
                }
            }
        }

        cancel_list(){
            var str_shipment_ids = ''
            this.selected_shipments.forEach(
                item => (str_shipment_ids = str_shipment_ids.concat(item,','))
                )
            var url = '/api/shipments/cancel/ids/'+str_shipment_ids;
            return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    location.reload(); 
                    self.update()
                }
            });
		}


	</script>
</search-shipment>