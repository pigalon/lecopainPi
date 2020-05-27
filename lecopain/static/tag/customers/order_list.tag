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
                    <th width="30%">client</th>
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
                    <td if={order.status == 'CREE'} width="6%" class="table-primary">{order.id}</td>
                    <td if={order.status == 'ANNULEE'} width="6%" class="table-dark">{order.id}</td>
                    <td if={order.status == 'TERMINEE'} width="6%" class="table-success">{order.id}</td>
                    <td if={order.status == 'DEFAUT'} width="6%" class="table-danger">{order.id}</td>
                    <td width="20%">{moment(order.shipping_dt).format('Do MMMM YYYY' )}</td>
                    <td width="30%">{order.customer_name}</td>
                    <td width="30%">{order.seller_name}</td>
                    <td width="20%"><span if={order.shipping_status == 'OUI'} style="color:green" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={order.shipping_status == 'NON'} style="color:grey" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={order.payment_status == 'OUI'} style="color:green" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={order.payment_status == 'NON'} style="color:grey" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={order.subscription_id != None} style="color:blue" ><i class="fas fa-clipboard-list"></i></i></span>
                    </td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <script>

		var self = this

        customer_id =  opts.customer_id
        

        moment.locale('fr');

		this.on('mount', function() {
			this.load_orders(customer_id)
            const location  = $('window.location')
		});

		/******************************************/
       	// load orders list
    	/*******************************************/
		load_orders(customer_id){
            var order_url = '/api/orders/customers/'+customer_id;

			$.ajax({
					url: order_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.orders = data['orders']
                        self.update()
					}
				});
		}
        show_order(order_id){
            return function(e) {
                console.log('show' + order_id)
                location = "/orders/"+order_id;
            }
		}

	</script>
</order-list>