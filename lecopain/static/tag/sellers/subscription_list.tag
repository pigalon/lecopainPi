<subscription-list>
    <br>
    <div class="card-header text-white bg-info">
        Liste des abonnements
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
                    <td width="64%">du <b>{moment(subscription.start_dt).format('Do MMMM YYYY' )}</b> au <b>{moment(subscription.end_dt).format('Do MMMM YYYY' )}</b></td>
                    <td width="30%">{subscription.customer_name}</td>
                    </td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <script>

		var self = this

        seller_id =  opts.seller_id
        

        moment.locale('fr');

		this.on('mount', function() {
			this.load_subscriptions(seller_id)
            const location  = $('window.location')
		});

		/******************************************/
       	// load subscriptions list
    	/*******************************************/
		load_subscriptions(seller_id){
            var subscription_url = '/api/subscriptions/sellers/'+seller_id;

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
        show_subscription(subscription_id){
            return function(e) {
                location = "/subscriptions/"+subscription_id;
            }
		}

	</script>
</subscription-list>