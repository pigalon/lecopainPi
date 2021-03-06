<product-line>
            <div class="form-group">
                Choix du produit à ajouter à la commande
                <div data-toggle="fieldset" id="product-fieldset">
                    <input type="hidden" name="row_nb" id="row_nb" value=0 />
                    <table width="50%">
                        <tr>
                            <td>
                                <select class="form-control" id="product_id" name="product_id" ref="product">
									<option each="{ product in products }" value={product.id}> {product.name}  - {product.price.toFixed(2)}</option>
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
                            <td width="30%"><input type="hidden" name="price[]" value="{line.price}"/>{line.price.toFixed(2)} €</td>
                            <td width="10%"><button type="button" id="remove" onclick="{remove_line}" class="btn btn-warning" ><i class="fa fa-minus"></i></button></td>
                        </tr>
                    </table>
                </div>
            </div>
			<div class="form-group">
                <input  id="Button" ref="submit_button" class="btn btn-outline-info" value="Valider" type="submit"/>
				<span class="left" style="color:red">{ message_validation }</span>
            </div>


	<script>
		this.val = 'start';

		lines = []
		cpt=0
		price=0
		product_name=''

		var self = this

		seller_id =  opts.seller_id
		page_lines = opts.lines

    	moment.locale('fr');

		this.on('mount', function() {
			page_lines = page_lines.replaceAll("'", "\"")
			this.load_lines()
			this.load_products()
      		const location  = $('window.location')
			if(self.refs.line_product_id == undefined){
				message_validation = 'Veuillez saisir au moins un article!'
				self.refs.submit_button.disabled = true
			}
			else{
				message_validation = ''
				self.refs.submit_button.disabled = false
			}
		});
		this.on('update', function() {
			if(self.refs.line_product_id == undefined){
				message_validation = 'Veuillez saisir au moins un article!'
				self.refs.submit_button.disabled = true
			}
			else{
				message_validation = ''
				self.refs.submit_button.disabled = false
			}
		});


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
				self.update()
			}

		}
		remove_line(e) {
			lines = lines.filter(function(line) {
				lines.splice(line.id, 1)
			})
			self.update()
		}

		load_lines()
		{
			items = JSON.parse(page_lines)

			items.forEach((item) => {
				cpt = cpt + 1;
				line =  {id : cpt, product_id:item.product_id, product_name:item.product_name, quantity:item.quantity,  price : item.price};
				lines.push(line)
			});
			self.update()
		}




		/******************************************
       	load products list
    	*******************************************/
		load_products(seller_id){
			var url = '/api/products/sellers/'+seller_id;
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
	</script>
</product-line>;
