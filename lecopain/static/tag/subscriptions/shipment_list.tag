<shipment-list>
    <p>
        <h4>Liste des livraisons </h4>
    </p>
    <table id="shipments_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="20%">date</th>
                    <th width="30%">client</th>
                    <th width="20%">Status</th>
                    <th width="20%">Liv.</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ shipment in shipments }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_shipment(shipment.id) }>
                <tr>
                    <td if={shipment.status == 'CREE' && shipment.updated_at == None} width="6%" class="table-primary">{shipment.id}</td>
                    <td if={shipment.status == 'CREE' && shipment.updated_at != None} width="6%" class="table-warning">{shipment.id}</td>
                    <td if={shipment.status == 'ANNULEE'} width="6%" class="table-dark">{shipment.id}</td>
                    <td if={shipment.status == 'TERMINEE'} width="6%" class="table-success">{shipment.id}</td>
                    <td if={shipment.status == 'DEFAUT'} width="6%" class="table-danger">{shipment.id}</td>

                    <td width="20%">{moment(shipment.shipping_dt).format('ddd Do MMMM' )}</td>
                    <td width="30%">{shipment.customer_name}</td>
                    <td width="20%"><span if={shipment.shipping_status == 'OUI'} style="color:green" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={shipment.shipping_status == 'NON'} style="color:grey" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={shipment.payment_status == 'OUI'} style="color:green" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={shipment.payment_status == 'NON'} style="color:grey" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={shipment.subscription_id != None} class="badge badge-warning">Ab.</span>
                    </td>
                    <td width="20%">
                        {shipment.shipping_price.toFixed(2)} €
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
                <a if={ (start - limit) > 0 } role="button" onclick="{load_shipments_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Livraisons précédentes </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ (start + limit) <= count } role="button" onclick="{load_shipments_next}"  style="color:white" class="btn btn-primary display:inline-block"> Livraisons suivantes <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>
    <br>
    <br>
    <script>

		var self = this
        var next_start = 0
        var previous_start = 0
        var limit = 10
        var start= 1
        var next_url = ''

        moment.locale('fr');

        subscription_id =  opts.subscription_id

		this.on('mount', function() {
			this.load_shipments(subscription_id)
            const location  = $('window.location')
		});

		/******************************************/
       	// load products list
    	/*******************************************/
		load_shipments(subscription_id){
             var shipment_url = '/api/shipments/subscriptions/'+subscription_id;
			$.ajax({
					url: shipment_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.shipments = data['results']
                        self.count = data['count']
                        self.limit = data['limit']
                        self.start = data['start']
                        self.next_start = parseInt(data['start'])+parseInt(limit)
                        self.previous_start = parseInt(data['start'])-parseInt(limit)
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
                    self.limit = data['limit']
                    self.start = data['start']
                    self.next_start = parseInt(data['start'])+parseInt(limit)
                    self.previous_start = parseInt(data['start'])-parseInt(limit)
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
                    self.limit = data['limit']
                    self.start = data['start']
                    console.log('start :' + self.start)
                    self.next_start = parseInt(data['start'])+parseInt(limit)
                    self.previous_start = parseInt(data['start'])-parseInt(limit)
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        show_shipment(shipment_id){
            return function(e) {
                location = "/shipments/"+shipment_id;
            }
		}

	</script>
</shipment-list>