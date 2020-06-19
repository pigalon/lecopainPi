<search-product>
    <div class="form-group">
        Vendeur :<br>
        <select onchange={ load_products } class="form-control" name="seller_id" id="seller_id" ref="seller_id" style="width: 12rem; display:inline-block" >
            <option value="0" SELECTED>Tous</option>
            <option each="{ seller in sellers }" value={seller.id}>{seller.name} </option>
        </select>
        <div class="right">
            <a role="button" href="/products/new" class="btn btn-primary display:inline-block">Ajouter</i></a>
        </div>
    </div>
    <table id="products_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="29%">Nom</th>
                    <th width="20%">Prix</th>
                    <th width="20%">Catégorie</th>
                    <th width="35%">Description</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ product in products }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_product(product.id) }>
                <tr>
                    <td width="6%" class="table-primary">{product.id}</td>
                    <td width="29%">{product.name} - {product.short_name}</td>
                    <td width="20%">{product.price}€</td>
                    <td width="20%">{product.category}</td>
                    <td width="25%">{product.description}</td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ (start - limit) > 0 } role="button" onclick="{load_products_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Produits précédents </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ (start + limit) <= count } role="button" onclick="{load_products_next}"  style="color:white" class="btn btn-primary display:inline-block"> Produits suivants <i class="fas fa-arrow-right"></i> </a>
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
            var ajaxCall_sellers = self.load_sellers();
			ajaxCall_sellers.done(function(data) {
				$(self.refs.seller_id).select2();
			})
            this.load_products()
            const location  = $('window.location')
		});

		/******************************************/
       	// load products list
        /*******************************************/
		load_products(){
            var product_url = '/api/products/';
            var seller_id = self.refs.seller_id.value;

            product_url = product_url.concat('sellers/',seller_id);

			$.ajax({
					url: product_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.products = data['results']
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
        load_products_next(){
            var product_url = self.next_url;

			$.ajax({
                url: product_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.products = data['results']
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
        load_products_previous(){
            var product_url = self.previous_url;

			$.ajax({
                url: product_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.products = data['results']
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
        show_product(product_id){
            return function(e) {
                location = "/products/"+product_id;
            }
		}
        load_sellers(){
			var url = '/api/sellers/';
			return $.ajax({
					url: url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.sellers = data['results']
                        self.update()
					}
				});
		}

	</script>
</search-product>