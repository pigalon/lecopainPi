<order-list>
    <br>
    <div class="card-header text-white bg-info">
        Liste des commandes
    </div>

    <table id="orders_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="20%">date</th>
                    <th width="30%">Client</th>
                    <th width="30%">Vendeur</th>
                    <th width="20%">Status</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ order in orders }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_order(order.id) }>
                <tr>
                    <td if={order.status == 'CREE' && order.updated_at == None} width="6%" class="table-primary">{order.id}</td>
                    <td if={order.status == 'CREE' && order.updated_at != None} width="6%" class="table-warning">{order.id}</td>
                    <td if={order.status == 'ANNULEE'} width="6%" class="table-dark">{order.id}</td>
                    <td if={order.status == 'TERMINEE'} width="6%" class="table-success">{order.id}</td>
                    <td if={order.status == 'DEFAUT'} width="6%" class="table-danger">{order.id}</td>
                    <td width="20%">{moment(order.shipping_dt).format('ddd MMMM' )}</td>
                    <td width="30%">{order.customer_name}</td>
                    <td width="30%">{order.seller_name}</td>
                    <td width="20%"><span if={order.shipping_status == 'OUI'} style="color:green" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={order.payment_status == 'OUI'} style="color:green" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={order.payment_status == 'NON'} style="color:grey" ><i class="fas fa-credit-card"></i></i></span>
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
                <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_orders_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Commandes précédentes </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ next_rul != '' && next_url != undefined } role="button" onclick="{load_orders_next}"  style="color:white" class="btn btn-primary display:inline-block"> Commandes suivantes <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>

    <script>

		var self = this
        var limit = 10
        var start= 1
        var next_url = ''
        var previous_url = ''


        seller_id =  opts.seller_id

        moment.locale('fr');

		this.on('mount', function() {
			this.load_orders(seller_id)
            const location  = $('window.location')
		});

		/******************************************/
       	// load orders list
    	/*******************************************/
		load_orders(seller_id){
            var order_url = '/api/orders/sellers/'+seller_id;

			$.ajax({
					url: order_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
                        self.orders = data['results']
                        self.count = data['count']
                        self.per_page = data['per_page']
                        self.page = data['page']
                        self.next_url = data['next']
                        self.previous_url = data['previous']
                        self.update()
					}
				});
		}
        load_orders_next(){
            var order_url = self.next_url;

			$.ajax({
                url: order_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.orders = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_orders_previous(){
            var order_url = self.previous_url;

			$.ajax({
                url: order_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.orders = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        show_order(order_id){
            return function(e) {
                location = "/orders/"+order_id;
            }
		}

	</script>
</order-list>