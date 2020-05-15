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
                            <td width="20%"><input type="hidden" , name="lines[][id]" value="{line.id}"/>{line.id}</td>
                            <td width="35%">{line.name}</td>
                            <td width="30%"><input type="number" style="width: 5em" name="lines[][quantities]" value="{line.quantity}"/></td>
                            <td width="30%">{line.price}</td>
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
			index = this.refs.product.selectedIndex
			text = this.refs.product[index].innerText;
			n = text.lastIndexOf(" - ");
			product_name = text.substr(0,n);
    		price = text.substr(n+3);
			cpt = cpt + 1;
			line =  {id : cpt, name : product_name, quantity : 1, price : price + " €"};
			lines.push(line)
		}
		remove_line(e) {
			lines = lines.filter(function(line) {
				lines.splice(line.id, 1)
			})
		}

		this.on('mount', function() {
			this.load_sellers()
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
