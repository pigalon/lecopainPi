<search-product>
    <div class="form-group">
        Vendeur:
        <select class="form-control" name="seller_id" id="seller_id" ref="seller_id" style="width: 12rem; display:inline-block" >
            <option value="0" SELECTED>Tous</option>
            <option each="{ seller in sellers }"  value={seller.id}>{seller.name} </option>
        </select>
        <select class="form-control" id="product_id" name="product_id" ref="product_id" style="width: 12rem; display:inline-block">
            <option value="0" SELECTED>Tous</option>
            <option each="{ product_name in product_names }" value={product_name.id}> {product_name.name} </option>
        </select>
        <button type="button" id="search" onclick="{load_products}" class="btn btn-primary" ><i class="fa fa-search"></i></button>

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
                    <th width="35%">Vendeur</th>
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
                    <td width="20%">{product.price.toFixed(2)}€</td>
                    <td width="20%">{product.category}</td>
                    <td width="25%">{product.seller_name}</td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_products_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Produits précédents </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_products_next}"  style="color:white" class="btn btn-primary display:inline-block"> Produits suivants <i class="fas fa-arrow-right"></i> </a>
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
            var ajaxCall_sellers = self.load_sellers();
			    ajaxCall_sellers.done(function(data) {
				$(self.refs.seller_id).select2();
			})

            var ajaxCall_product_names = self.load_product_names();
			    ajaxCall_product_names.done(function(data) {
				$(self.refs.product_id).select2();
			})
            //this.load_products()
            const location  = $('window.location')

            search_url = localStorage.getItem('search_product_url');
			if(search_url != null){
                this.load_products_from_url(search_url)
			}
		});

		/******************************************/
       	// load products list
        /*******************************************/
		load_products(){
            var product_url = '/api/products/';
            var seller_id = self.refs.seller_id.value;
            var product_id = self.refs.product_id.value;

            product_url = product_url.concat('sellers/',seller_id);

            if ( product_id != undefined && product_id != '0'){
                product_url = product_url.concat('/id/',product_id);
            }

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
			var url = '/api/products/';
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