<search-seller>
   <div class="form-group">
    <div class="right">
        <a role="button" href="/sellers/new" class="btn btn-primary display:inline-block">Ajouter</i></a>
    </div>
    </div>
    <table id="sellers_list" width="100%">
        <tr>
            <td>
                <table width="100%">
                    <tr>
                        <th width="6%">id</th>
                        <th width="44%">Nom</th>
                        <th width="50%">Email</th>
                    </tr>
                </table>
            </td>
        </tr>
        <tr each="{ seller in sellers }">
            <td>
                <table width="100%" class="table table-striped" onclick={ show_seller(seller.id) }>
                    <tr>
                        <td width="6%" class="table-primary">{seller.id}</td>
                        <td width="44%">{seller.name}</td>
                        <td width="44%">{seller.email}</td>
                    </tr>
                </table>
            </td>
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
            this.load_sellers()
            const location  = $('window.location')
		});

		/******************************************/
       	// load sellers list
        /*******************************************/
		load_sellers(){
            var seller_url = '/api/sellers/';
			$.ajax({
					url: seller_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.sellers = data['results']
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
        load_sellers_next(){
            var seller_url = self.next_url;

			$.ajax({
                url: seller_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.orders = data['results']
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
        load_sellers_previous(){
            var seller_url = self.previous_url;

			$.ajax({
                url: seller_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.orders = data['results']
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
        show_seller(seller_id){
            return function(e) {
                location = "/sellers/"+seller_id;
            }
		}

	</script>
</search-seller>