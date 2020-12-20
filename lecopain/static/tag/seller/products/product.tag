<search-product>
    <table id="products_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="29%">Nom</th>
                    <th width="20%">Prix</th>
                    <th width="20%">Catégorie</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ product in products }">
            <td>
            <table width="100%" class="table table-striped">
                <tr>
                    <td width="6%" class="table-primary">{product.id}</td>
                    <td width="29%">{product.name} - {product.short_name}</td>
                    <td width="20%">{product.price.toFixed(2)}€</td>
                    <td width="20%">{product.category}</td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_products_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> précédents </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_products_next}"  style="color:white" class="btn btn-primary display:inline-block"> suivants <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>
    <br>
    <br>
    <script>

		var self = this
        var limit = 30
        var start= 1
        var next_url = ''
        var previous_url = ''

        moment.locale('fr');

		this.on('mount', function() {
      this.load_products();
		});

		/******************************************/
       	// load products list
        /*******************************************/
		load_products(){
      var product_url = '/seller/api/products';

      localStorage.setItem('search_product_url', product_url);

      this.load_products_from_url(product_url);
		}

        load_products_from_url(product_url){

			$.ajax({
					url: product_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.products = data['results']
                        self.count = data['count']
                        self.per_page = data['per_page']
                        self.page = data['page']
                        self.next_url = data['next']
                        self.previous_url = data['previous']
                        self.update()
					}
				});
		}
        load_products_next(){
            var product_url = self.next_url;
            localStorage.setItem('search_product_url', product_url);

			$.ajax({
                url: product_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.products = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_products_previous(){
            var product_url = self.previous_url;
            localStorage.setItem('search_product_url', product_url);
			$.ajax({
                url: product_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.products = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_product_names(){
			var url = '/seller/api/products/';
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.product_names = data['products']
                    self.update()
                }
            });
		}
        show_product(product_id){
            return function(e) {
                location = "/seller/products/"+product_id;
            }
		}
	</script>
</search-product>