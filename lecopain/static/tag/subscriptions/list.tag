<search-subscription>
    <div class="form-group">
        Client :<br>
        <select onchange={ load_subscriptions } class="form-control" name="customer_id" id="customer_id" ref="customer_id" style="width: 12rem; display:inline-block" >
            <option value="0" SELECTED>Tous</option>
            <option each="{ customer in customers }" value={customer.id}>{customer.firstname} {customer.lastname}</option>
        </select><select onchange={ load_subscriptions } class="form-control" name="period" id="period" ref="period" style="width: 12rem; display:inline-block">
            <option value="day">Jour</option>
            <option value="week">Semaine</option>
            <option value="month">Mois</option>
            <option value="all">Toutes</option>
        </select>
        <div class="right">
            <a role="button" href="/subscriptions/new" class="btn btn-primary display:inline-block">Ajouter</i></a>
        </div>
    </div>
    <table id="subscriptions_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="64%">Période</th>
                    <th width="30%">client</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ subscription in subscriptions }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_subscription(subscription.id) }>
                <tr>
                    <td if={subscription.status == 'CREE'} width="6%" class="table-primary">{subscription.id}</td>
                    <td if={subscription.status == 'ANNULE'} width="6%" class="table-dark">{subscription.id}</td>
                    <td if={subscription.status == 'TERMINE'} width="6%" class="table-success">{subscription.id}</td>
                    <td if={subscription.status == 'DEFAUT'} width="6%" class="table-danger">{subscription.id}</td>
                    <td width="64%">du {moment(subscription.start_dt).format('Do MMMM YYYY' )} aua {moment(subscription.end_dt).format('Do MMMM YYYY' )}</td>
                    <td width="30%">{subscription.customer_name}</td>
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
			this.load_subscriptions()
            this.load_customers()
            const location  = $('window.location')
		});

		/******************************************/
       	// load products list
    	/*******************************************/
		load_subscriptions(){
            var subscription_url = '/api/subscriptions/';
            var customer_id = self.refs.customer_id.value;
            var period = self.refs.period.value;

            if (period == undefined){
                period = 'all'
            }

            subscription_url = subscription_url.concat('period/',period,'/');

            subscription_url = subscription_url.concat('customers/',customer_id);

			$.ajax({
					url: subscription_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.subscriptions = data['subscriptions']
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
        show_subscription(subscription_id){
            return function(e) {
                console.log('show' + subscription_id)
                location = "/subscriptions/"+subscription_id;
            }
		}

	</script>
</search-subscription>