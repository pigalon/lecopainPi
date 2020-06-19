<seller-product-line>

			<div class="form-group">
				<table width="100%">
                        <tr>
                            <td>
								Choix du vendeur :
							</td>
                            <td>
								Choix de la catégorie
							</td>
						</tr>
						<tr>
                            <td>
								<select class="form-control" id="seller_id" name="seller_id" ref="seller" onchange="{ load_products }" >
									<option each="{ seller in sellers }" value={seller.id}> {seller.name} </option>
								</select>
							</td>
                            <td>
								<select class="form-control" id="category" ref="category" name="category" onchange="{ load_products }" >
									<option each="{ category in categories }" value={category}> {category} </option>
								</select>
								<input type="hidden" id="category_name" name="category_name" ref="category_name" value={category} />
							</td>
						</tr>
			</div>
            <div class="form-group">
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
							<th width="25%">Vendeur</th>
                            <th width="30%">nom</th>
                            <th width="15%">quantité</th>
                            <th width="15%">prix</th>
                            <th width="10%"></th>
                        </tr>
						<tr each="{ line in lines }">
                            <td width="20%"><input type="hidden" ref="line_product_id" id="line_product_id" name="product_id[]" value="{line.product_id}"/ maxlength="2" readonly>{line.id}</td>
                            <td width="25%"><input type="hidden" ref="line_seller_id" id="line_seller_id" name="seller_id[]" value="{line.seller_id}"/ maxlength="2" readonly>{line.seller_name}</td>
							<td width="25%">{line.product_name}</td>
                            <td width="15%"><input type="number" style="width: 5em" ref="quantity" name="quantity[]" value="{line.quantity}"/></td>
                            <td width="15%"><input type="hidden" name="price[]" value="{line.price}"/>{line.price} €</td>
                            <td width="10%"><button type="button" id="remove" onclick="{remove_line}" class="btn btn-warning" ><i class="fa fa-minus"></i></button></td>
                        </tr>
                    </table>
                </div>
            </div>
			<div class="form-group">
                <input style="height:40px;width:120px" id="Button" ref="submit_button" class="btn btn-outline-info" value="Valider" onclick="{submit_shipment}"/>
				<span class="left" style="color:red">{ message_validation }</span>
            </div>


	<script>
		this.val = 'start';

		lines = []
		cpt=0
		price=0
		product_name=''

		var self = this

		page_lines = opts.lines

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
			index = this.refs.seller.selectedIndex;
			seller_id = this.refs.seller.value;
			seller_name = this.refs.seller[index].innerText;
			
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
				line =  {id : cpt, product_id:product_id, product_name:product_name, seller_id:seller_id, seller_name:seller_name, quantity : 1, price : price};
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

		String.prototype.replaceAll = function(str1, str2, ignore)
		{
    		return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
		}

		this.on('mount', function() {
			if(page_lines != undefined){
				page_lines = page_lines.replaceAll("'", "\"")
				this.load_lines(page_lines)
			}

			var ajaxCall_seller = self.load_sellers()
			var ajaxCall_categories = self.load_categories()
			ajaxCall_seller.done(function(data1) {
				ajaxCall_categories.done(function(data2) {
					var ajaxCall_product = self.load_products();
					ajaxCall_product.done(function(data3) {
						$(self.refs.product).select2();
					})
				})
			});
			if(self.refs.line_product_id == undefined){
				message_validation = 'Veuillez saisir au moins un article!'
				self.refs.submit_button.disabled = true
				self.refs.category.disabled = false
			}
			else{
				message_validation = ''
				self.refs.submit_button.disabled = false
				self.refs.category.disabled = true
			}
		});

		this.on('update', function() {
			if(self.refs.line_product_id == undefined){
				message_validation = 'Veuillez saisir au moins un article!'
				self.refs.submit_button.disabled = true
				self.refs.category.disabled = false
			}
			else{
				message_validation = ''
				self.refs.submit_button.disabled = false
				self.refs.category.disabled = true
			}
		});

		/******************************************
       	load products list
    	*******************************************/
		load_products(){
			seller_id =  this.refs.seller.value
			category =  this.refs.category.value

			var url = '/api/products/sellers/'+seller_id+'/categories/'+category;
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
					self.sellers = data['results']
					self.update()
				}
			});
		}

		load_categories(){
			var url = '/api/products/categories';
			return $.ajax({
					url: url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.categories = data['categories']
						self.update()
					}
				});
		}

		load_lines(page_lines)
		{
			console.log('page_lines :'+ page_lines)
			items = JSON.parse(page_lines)

			items.forEach((item) => {
				cpt = cpt + 1;
				line =  {id : cpt, product_id:item.product_id, product_name:item.product_name, seller_id:item.seller_id, seller_name:item.seller_name, quantity:item.quantity,  price : item.price};
				lines.push(line)
			});
			self.update()
		}

		submit_shipment(){
			this.refs.seller.disabled = false
			document.getElementById("shipment_form").submit();
		}
	</script>
</seller-product-line>;
