<shipment-list>
    <p>
        <h4>Liste des livraisons prévues pour cet abonnement</h4>
    </p>
    <table id="shipments_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="20%">date</th>
                    <th width="10%">Liv.</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ shipment in shipments }">
            <td>
            <table width="100%" class="table table-striped">
                <tr>
                    <td onmouseover="changeBackgroundColor(this)" onmouseout="restoreBackgroundColor(this)" style="cursor: pointer" onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE'} width="6%" class="table-primary">{shipment.id}</td>
                    <td if={shipment.status == 'DEFAUT'} width="6%" class="table-danger">{shipment.id}</td>

                    <td width="20%">{moment(shipment.shipping_dt).format('ddd Do MMM' )}</td>

                    <td if={shipment.status == 'ANNULEE'} width="10%" >0.00 €</td>
                    <td if={shipment.status != 'ANNULEE'} width="10%">
                        {shipment.shipping_price.toFixed(2)} €
                    </td>

                </tr>
            </table>
            </td>
        </tr>
        <tr>
            <table width="100%" >
                <tr class="bg-warning">
                    <td width="6%">
                    </td>
                    <td width="20%">
                    </td>
                    <td width="30%">
                    </td>
                    <td width="15%">
                    </td>
                    <td width="10%">
                        = {shipping_sum.toFixed(2)} €
                    </td>
                    <td width="15%">
                    </td>
                </tr>
            </table>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ previous_url != '' && previous_url != undefined}  role="button" onclick="{load_shipments_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Livraisons précédentes </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_shipments_next}"  style="color:white" class="btn btn-primary display:inline-block"> Livraisons suivantes <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>
    <br>
    <br>
    <script>

		var self = this
        var per_page = 10
        var page= 1
        var next_url = ''
        var previous_url = ''
        shipping_sum = 0.0

        moment.locale('fr');
        this.selected_shipments = []

        subscription_id =  opts.subscription_id

		this.on('mount', function() {
			this.load_shipments(subscription_id);
            const location  = $('window.location')
		});

		/******************************************/
       	// load products list
    	/*******************************************/
		load_shipments(subscription_id){
            var shipment_url = '/api/customer/shipments/subscriptions/'+subscription_id;
			return $.ajax({
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
                        self.shipping_sum = 0.0
                        self.shipments.forEach((shipment) => {
                            if(shipment.status != 'ANNULEE'){
                                self.shipping_sum = shipment.shipping_price  + self.shipping_sum;
                            }
                        });

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
                    self.shipping_sum = 0.0
                        self.shipments.forEach((shipment) => {
                            if(shipment.status != 'ANNULEE'){
                                self.shipping_sum = shipment.shipping_price  + self.shipping_sum;
                            }
                        });
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
                    self.shipping_sum = 0.0
                        self.shipments.forEach((shipment) => {
                            if(shipment.status != 'ANNULEE'){
                                self.shipping_sum = shipment.shipping_price  + self.shipping_sum;
                            }
                        });
                    self.update()
                }
            });
		}
        show_shipment(shipment_id){
            return function(e) {
                location = "/customer/shipments/"+shipment_id;
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

	</script>
</shipment-list>