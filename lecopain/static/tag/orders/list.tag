<search-order>
    <div class="form-group">
        Client :<br>
        <button type="button" id="more_fields" onclick="{ load_orders }" class="btn btn-primary display:inline-block" ><i class="fa fa-search"></i></button>
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
                    <th width="20%">Actions</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ order in orders }">
            <td>
            <table width="100%" class="table table-striped">
                <tr>

                    <td if={order.status == 'CREE'} width="6%" class="table-primary">{order.id}</td>
                    <td if={order.status == 'ANNULEE'} width="6%" class="table-dark">{order.id}</td>
                    <td if={order.status == 'TERMINEE'} width="6%" class="table-success">{order.id}</td>
                    <td if={order.status == 'DEFAUT'} width="6%" class="table-danger">{order.id}</td>
                    <td width="20%">{moment(order.shipping_dt).format('Do MMMM YYYY' )}</td>
                    <td width="30%">{order.customer_name}</td>
                    <td width="30%">{order.seller_name}</td>
                    <td width="20%"><a href="/orders/{order.id}" class="text-dark" alt="Détails"><i class="fas fa-eye"></i></a></span>
                    <a href="/orders/update/{order.id}" class="text-secondary" alt="Editer"><i class="fas fa-edit"></i></a>
                    <a href="/orders/delete/{order.id}" class="text-danger" alt="Supprimer"><i class="fas fa-trash-alt"></i></a></td>
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
		});

		/******************************************/
       	// load products list
    	/*******************************************/
		load_orders(){
			var url = 'http://localhost:5000/_getjs_orders/';
			$.ajax({
					url: url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.orders = data['orders']
                        self.update()
					}
				});
		}
	</script>
</search-order>