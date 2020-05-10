<my-select>

			<div class="form-group">
				Choix du vendeur :
				<select class="form-control" id="seller_id" name="seller_id" ref="seller" onchange="{ load_products }">
					<option each="{ seller in sellers }" value={seller.id}> {seller.name} </option>
                </select>
			</div>
            <div class="form-group">
                Choix du produit à ajouter à la commande
                <div data-toggle="fieldset" id="product-fieldset">
                    <input type="hidden" name="row_nb" id="row_nb" value=0 />
                    <table width="50%">
                        <tr>
                            <td>
                                <select class="form-control" id="product_id" name="product_id" ref="product">
									<option each="{ product in products }" value={product.id}> {product.name}  - {product.price}</option>
                                </select>
                            </td>
                            <td>
                                <button type="button" id="more_fields" onclick="add_fields();" class="btn btn-primary" ><i class="fa fa-plus"></i></button>
                            </td>
                        </tr>
                    </table>
                    <table id="tab_qn_ans" width="100%">
                        <tr>
                            <th width="20%">id</th>
                            <th width="35%">nom</th>
                            <th width="30%">quantité</th>
                            <th width="30%">prix</th>
                            <th width="10%"></th>
                        </tr>
                    </table>
                </div>
            </div>


	<script>
		this.val = 'start';

		var self = this

		change(e) 
		{
			this.val = "change!"
		}
		up(e) 
		{
			this.val = "up"
		}

		this.on('mount', function() {
			this.load_sellers()
			console.log(this.refs.items); // [div#alpha, div#beta]
		});

		/******************************************
       	load products list
    	*******************************************/
		load_products(){
			seller_id =  this.refs.seller.value
			var url = 'http://localhost:5000/_getjs_products/'+seller_id;
			$.ajax({
					url: url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.products = data['products']
						self.update()
					}
				});
			 
		}
		/******************************************
		load sellers list
		*******************************************/

		load_sellers(){
		var url = 'http://localhost:5000/_getjs_sellers/'; 
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
</my-select>;
