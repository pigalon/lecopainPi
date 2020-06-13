<search-shipment>
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

                    <td width="20%">{moment(shipment.shipping_dt).format('Do MMMM YYYY' )}</td>
                    <td width="30%">{shipment.customer_name}</td>
                    <td width="20%"><span if={shipment.shipping_status == 'OUI'} style="color:green" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={shipment.shipping_status == 'NON'} style="color:grey" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={shipment.payment_status == 'OUI'} style="color:green" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={shipment.payment_status == 'NON'} style="color:grey" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={shipment.subscription_id != None} class="badge badge-warning">Ab.</span>
                    </td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <script>

		var self = this

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
             var shipment_url = '/api/shipements/subscriptions/'+subscription_id;
			$.ajax({
					url: shipment_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.shipments = data['data']
                        self.update()
					}
				});
		}
        show_shipment(shipment_id){
            return function(e) {
                console.log('show' + shipment_id)
                location = "/shipments/"+shipment_id;
            }
		}

	</script>
</search-shipment>