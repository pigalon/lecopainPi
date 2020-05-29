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
                    <th width="24%">Nom</th>
                    <th width="20%">Prix</th>
                    <th width="20%">Catégorie</th>
                    <th width="30%">Description</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ product in products }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_product(product.id) }>
                <tr>
                    <td width="6%" class="table-primary">{product.id}</td>
                    <td width="24%">{product.name}</td>
                    <td width="20%">{product.price}€</td>
                    <td width="20%">{product.category}</td>
                    <td width="30%">{product.description}</td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <script>

		var self = this

        moment.locale('fr');

		this.on('mount', function() {
            this.load_sellers()
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
						self.products = data['products']
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
			$.ajax({
					url: url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.sellers = data['sellers']
                        self.update()
					}
				});
		}

	</script>
</search-product>