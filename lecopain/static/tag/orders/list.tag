<search-order>
    <div class="form-group">
        Client :<br>
        <select onchange={ load_orders } class="form-control" name="customer_id" id="customer_id" ref="customer_id" style="width: 12rem; display:inline-block" >
            <option value="0" SELECTED>Tous</option>
            <option each="{ customer in customers }" value={customer.id}>{customer.firstname} {customer.lastname}</option>
        </select><select onchange={ load_orders } class="form-control" name="period" id="period" ref="period" style="width: 12rem; display:inline-block">
            <option value="day">Jour</option>
            <option value="week">Semaine</option>
            <option value="month">Mois</option>
            <option value="all">Toutes</option>
        </select>
        <div class="right">
            <a role="button" href="/orders/new" class="btn btn-primary display:inline-block">Ajouter</i></a>
        </div>
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
                    </td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <script>

		var self = this

        moment.locale('fr');

		this.on('mount', function() {
			this.load_orders()
            this.load_customers()
            const location  = $('window.location')
		});

		/******************************************/
       	// load products list
    	/*******************************************/
		load_orders(){
            var order_url = '/api/orders/';
            var customer_id = self.refs.customer_id.value;
            var period = self.refs.period.value;

            if (period == undefined){
                period = 'all'
            }

            order_url = order_url.concat('period/',period,'/');

            order_url = order_url.concat('customers/',customer_id);

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
        load_customers(){
			var url = '/api/customers/';
			$.ajax({
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
        show_order(order_id){
            return function(e) {
                console.log('show' + order_id)
                location = "/orders/"+order_id;
            }
		}

	</script>
</search-order>