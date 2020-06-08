<search-report>
    <div class="form-group">
        <table id="orders_list" width="100%">
            <tr>
                <td>Vendeur :</td><td>Date</td><td>Durée</td><td></td>
            </tr>
            <tr>
                <td>
                    <select class="form-control" id="seller_id" name="seller_id" ref="seller_id">
					    <option each="{ seller in sellers }" value={seller.id}> {seller.name} </option>
                    </select>
                </td>
                <td>
                    <input type="text" name="day" ref="day" id="datepicker_day" data-language='fr' class="form-control datepicker-input" />
                </td>
                <td>
                    <select class="form-control" name="period" id="period" ref="period" style="width: 12rem; display:inline-block">
                        <option value="day">Jour</option>
                        <option value="week">Semaine</option>
                        <option value="all">Toutes</option>
                    </select>
                </td>
                <td>
                    <button type="button" id="search" onclick="{search}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
                </td>
            </tr>
        </table>
        <ul class="list-group" width="100%">
            <li class="list-group-item" width="100%">
                <span class="btn btn-warning">Totaux Période</span> -  <b>Nb commandes</b> : <span class="btn btn-warning">x{amounts['nb_orders']}</span> - <b>Nb articles</b> : <span class="btn btn-warning">x{amounts['nb_products']}</span> - <b>Montant total</b> : <span class="btn btn-warning">{amounts['price']}€</span> - <b>Livraison total</b> : <span class="btn btn-warning">{amounts['shipping_price']}€</span>
                <table class="table table-bordered">
                    <tr>
                        <td each="{product in amounts['products']}">
                            {product['short_name']}: x{product['quantity']}
                        </td>
                    </tr>
                </table>

            <li width="100%" class="list-group-item" each="{day_report, index in days}">
                <table><tr>
                <td> <span style="width: 200px; display: block;" class="btn btn-secondary">{moment(day_report['date']).format('dddd Do MMMM' ) }</span> </td> <td>-  <b>Nb commandes</b> : x{day_report['amount']['nb_orders']} - <b>Nb articles</b> : x{day_report['amount']['nb_products']} - <b>Montant total</b> : {day_report['amount']['price']}€ - <b>Livraison total</b> : {day_report['amount']['shipping_price']}€</td>
                <table class="table table-bordered" style="margin-bottom: 0px; padding-bottom: 0px">
                    <tr class="table-secondary">
                        <td each="{product in day_report['amount']['products']}">
                            {product['short_name']}: x{product['quantity']}
                        </td>
                    </tr>
                </table>
                <table class="table table-bordered" style="margin-top: 0px; padding-top: 0px">
                    <tr each="{line in day_report['lines']}">
                        <td class="table-primary" width="15%">
                            {line['customer']}
                        </td>
                        <td>
                            <span each="{product in line['products']}">
                                {product['name']}: x{product['quantity']},
                            </span>
                        </td>
                    </tr>
                </table>
            </li>
        </ul>

    <script>

        $(function () {
            $("#datepicker_day").datepicker();
        });

		var self = this
        days=[]
        amounts={}
        //day_report={'amount',}

        moment.locale('fr');

		this.on('mount', function() {
            this.load_sellers()
		});

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
					self.update()
				}
			});
		}

        String.prototype.replaceAll = function(str1, str2, ignore)
		{
    		return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
		}

        search(){
            this.search_days();
            this.search_amounts();
        }

        search_days(){
            var url = '/api/reports/days/'
            
            var seller_id = self.refs.seller_id.value;
            var period = self.refs.period.value;
            var day = self.refs.day.value;

            url = url.concat('period/',period,'/');
            url = url.concat('date/', day.replaceAll("/",""),'/');
            url = url.concat('sellers/',seller_id);

            return $.ajax({
				url: url,
				type: "GET",
				dataType: "json",
				contentType: "application/json; charset=utf-8",
				success: function(data) {
					self.days = data['days']
					self.update()
				}
			});
            
        }
        search_amounts(){
            var url = '/api/reports/amounts/'
            
            var seller_id = self.refs.seller_id.value;
            var period = self.refs.period.value;
            var day = self.refs.day.value;

            url = url.concat('period/',period,'/');
            url = url.concat('date/', day.replaceAll("/",""),'/');
            url = url.concat('sellers/',seller_id);

            return $.ajax({
				url: url,
				type: "GET",
				dataType: "json",
				contentType: "application/json; charset=utf-8",
				success: function(data) {
					self.amounts = data['amounts']
					self.update()
				}
			});
            
        }

	</script>
</search-report>