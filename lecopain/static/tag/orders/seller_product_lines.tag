<seller-product-line>

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
                                <button type="button" id="more_fields" onclick="{add_line}" class="btn btn-primary" ><i class="fa fa-plus"></i></button>
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
						<tr each="{ line in lines }">
                            <td width="20%"><input type="hidden" ref="line_product_id" id="line_product_id" name="product_id[]" value="{line.product_id}"/ maxlength="2" readonly>{line.id}</td>
                            <td width="35%">{line.product_name}</td>
                            <td width="30%"><input type="number" style="width: 5em" ref="quantity" name="quantity[]" value="{line.quantity}"/></td>
                            <td width="30%"><input type="hidden" name="price[]" value="{line.price}"/>{line.price} €</td>
                            <td width="10%"><button type="button" id="remove" onclick="{remove_line}" class="btn btn-warning" ><i class="fa fa-minus"></i></button></td>
                        </tr>
                    </table>
                </div>
            </div>


	<script>
		this.val = 'start';

		lines = []
		cpt=0
		price=0
		product_name=''
		first_seller_id=0

		var self = this

		change(e) 
		{
			this.val = "change!"
		}
		up(e) 
		{
			this.val = "up"
		}

		add_line(e)
		{
			index = this.refs.product.selectedIndex;
			text = this.refs.product[index].innerText;
			product_id = this.refs.product.value;
			line_product_ids = this.refs.line_product_id

			b_add_new_line = true // we will determine if there is already a line with the same produt_id

			if(line_product_ids != undefined){
				if(line_product_ids.length == undefined){
					if(product_id == line_product_ids.value){ // only one already existing line is equal
						b_add_new_line = false
						this.refs.quantity.value = parseInt(this.refs.quantity.value) + 1
					}
			    }
				else{
					for(i=0; i<(line_product_ids.length); i++){
						if(product_id == line_product_ids[i].value){
							b_add_new_line = false
							this.refs.quantity[i].value = parseInt(this.refs.quantity[i].value) + 1
						}
					}
				}
			}

			if(b_add_new_line){ // add line only if not already existing
				n = text.lastIndexOf(" - ");
				product_name = text.substr(0,n);
				price = text.substr(n+3);
				cpt = cpt + 1;
				line =  {id : cpt, product_id:product_id, product_name:product_name, quantity : 1, price : price};
				lines.push(line)
			}

		}
		remove_line(e) {
			lines = lines.filter(function(line) {
				lines.splice(line.id, 1)
			})
		}

		this.on('mount', function() {
			var ajaxCall = self.load_sellers()
			ajaxCall.done(function(data) {
				self.load_products();
			});

						

		});



		/******************************************
       	load products list
    	*******************************************/
		load_products(){
			seller_id =  this.refs.seller.value

			var url = '/api/products/sellers/'+seller_id;
			return $.ajax({
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
		var url = '/api/sellers/';
		return $.ajax({
				url: url,
				type: "GET",
				dataType: "json",
				contentType: "application/json; charset=utf-8",
				success: function(data) {
					self.sellers = data['sellers']
					first_seller_id = data['sellers'][0].id
					self.update()
				}
			});
		}
	</script>
</seller-product-line>;
