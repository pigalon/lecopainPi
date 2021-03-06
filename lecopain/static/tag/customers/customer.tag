<search-customer>
    <div class="form-group">
        Villes:
        <br>
        <select onchange={ load_customers } class="form-control" name="city" id="city" ref="city" style="width: 12rem; display:inline-block" >
            <option value="all" SELECTED>Toutes</option>
            <option each="{ city in cities }" value={city}>{city} </option>
        </select>
        <select class="form-control" id="customer_id" name="customer_id" ref="customer_id" style="width: 12rem; display:inline-block">
            <option value="0" SELECTED>Tous</option>
            <option each="{ customer_name in customer_names }" value={customer_name.id}> {customer_name.firstname} {customer_name.lastname} </option>
        </select>
        <button type="button" id="search" onclick="{load_customers}" class="btn btn-primary" ><i class="fa fa-search"></i></button>

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
                <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_customers_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Clients précédents </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_customers_next}"  style="color:white" class="btn btn-primary display:inline-block"> Clients suivants <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>
    <br>
    <br>
    <script>

		var self = this
        var limit = 10
        var start= 1
        var next_url = ''
        var previous_url = ''

        moment.locale('fr');

		this.on('mount', function() {
            
            var ajaxCall_cities = self.load_cities();
			ajaxCall_cities.done(function(data) {
				$(self.refs.city).select2();
			})

            var ajaxCall_customer_names = self.load_customer_names();
			ajaxCall_customer_names.done(function(data) {
				$(self.refs.customer_id).select2();
			})
            
            const location  = $('window.location')

            search_url = localStorage.getItem('search_customer_url');
			if(search_url != null){
                this.load_customers_from_url(search_url)
			}
		});

		/******************************************/
       	// load products list
        /*******************************************/
		load_customers(){
            var customer_url = '/api/customers/';
            var city = self.refs.city.value;
            var customer_id = self.refs.customer_id.value;

            if (city == undefined){
                city = 'all'
            }

            customer_url = customer_url.concat('cities/',city);

            if ( customer_id != undefined && customer_id != '0'){
                customer_url = customer_url.concat('/id/',customer_id);
            }

            localStorage.setItem('search_customer_url', customer_url);

			this.load_customers_from_url(customer_url)
		}
        
        load_customers_from_url(customer_url){

			$.ajax({
					url: customer_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.customers = data['results']
                        self.count = data['count']
                        self.per_page = data['per_page']
                        self.page = data['page']
                        self.next_url = data['next']
                        self.previous_url = data['previous']
                        self.update()
					}
				});
		}
        load_customers_next(){
            var customer_url = self.next_url;
            localStorage.setItem('search_customer_url', customer_url);

			$.ajax({
                url: customer_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.customers = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_customers_previous(){
            var customer_url = self.previous_url;
            localStorage.setItem('search_customer_url', customer_url);

			$.ajax({
                url: customer_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.customers = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_cities(){
			var url = '/api/customers/cities';
			return $.ajax({
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
        load_customer_names(){
			var url = '/api/customers/';
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.customer_names = data['customers']
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