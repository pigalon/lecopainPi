<search-customer>
    <div class="form-group">
        Ville :<br>
        <select onchange={ load_customers } class="form-control" name="city" id="city" ref="city" style="width: 12rem; display:inline-block" >
            <option value="all" SELECTED>Toutes</option>
            <option each="{ city in cities }" value={city}>{city} </option>
        </select>
        <div class="right">
            <a role="button" href="/customers/new" class="btn btn-primary display:inline-block">Ajouter</i></a>
        </div>
    </div>
    <table id="customers_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="44%">Nom - Prénom</th>
                    <th width="20%">Code Postal</th>
                    <th width="30%">Ville</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ customer in customers }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_customer(customer.id) }>
                <tr>
                    <td width="6%" class="table-primary">{customer.id}</td>
                    <td width="44%">{customer.firstname} {customer.lastname}</td>
                    <td width="20%">{customer.cp}</td>
                    <td width="30%">{customer.city}</td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ (start - limit) > 0 } role="button" onclick="{load_customers_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Clients précédents </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ (start + limit) <= count } role="button" onclick="{load_customers_next}"  style="color:white" class="btn btn-primary display:inline-block"> Clients suivants <i class="fas fa-arrow-right"></i> </a>
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

		this.on('mount', function() {
            this.load_customers()
            this.load_cities()
            const location  = $('window.location')
		});

		/******************************************/
       	// load products list
        /*******************************************/
		load_customers(){
            var customer_url = '/api/customers/';
            var city = self.refs.city.value;

            if (city == undefined){
                city = 'all'
            }

            customer_url = customer_url.concat('cities/',city);

			$.ajax({
					url: customer_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.customers = data['results']
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
        load_customers_next(){
            var customer_url = self.next_url;

			$.ajax({
                url: customer_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.customers = data['results']
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
        load_customers_previous(){
            var customer_url = self.previous_url;

			$.ajax({
                url: customer_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.customers = data['results']
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
        load_cities(){
			var url = '/api/customers/cities';
			$.ajax({
					url: url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.cities = data['cities']
                        self.update()
					}
				});
		}
        show_customer(customer_id){
            return function(e) {
                console.log('show' + customer_id)
                location = "/customers/"+customer_id;
            }
		}

	</script>
</search-customer>