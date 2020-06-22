<search-report-shipment>
    <div class="form-group">
        Client:
        <br>
        <select class="form-control" id="customer_id" name="customer_id" ref="customer_id" style="width: 14rem; display:inline-block">
        <option value="0" SELECTED>Tous</option>
		    <option each="{ customer in customers }" value={customer.id}> {customer.firstname} {customer.lastname} </option>
        </select>
        <input type="text" style="width: 12rem; display:inline-block" name="day" ref="day" id="datepicker_day" data-language='fr' class="form-control datepicker-input" />
        <select class="form-control" name="period" id="period" ref="period" style="width: 12rem; display:inline-block">
            <option value="day">Jour</option>
            <option value="week">Semaine</option>
            <option value="all">Toutes</option>
        </select>
        <button type="button" id="search" onclick="{search_reports}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
        <br>
        
    </div>

    <h4>Total Période</h4> 
    <ul>
        <li><b>Nb Livraisons</b> : <span class="btn btn-warning">x{reports['nb_shipments']}</span> </li>
        <li><b>Nb Articles</b> : <span class="btn btn-warning">x{reports['nb_products']}</span></li>  
        <li><b>Montant Livraison total</b> : <span class="btn btn-warning">{reports['shipping_price']}€</span></li>
    </ul>
        <br><br>
        <h4>Liste des livraisons:</h4> 
        <br>
        <table class="table table-bordered table-striped">
            <tr each="{shipment in reports['shipments']}">
                <td>
                    <h5>Livraison N° : {shipment.id}</h5>
                    <p>Livré le : {moment(shipment.shipping_dt).format('ddd Do MMMM' )} <br>
                    Client :  {shipment.customer_name} <br>
                    Montant livraison :  {shipment.shipping_price} €</p>
                </td>
            </tr>
        </table>

       
    <script>

        String.prototype.replaceAll = function(str1, str2, ignore)
        {
            return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
        }

        $(function () {
            $("#datepicker_day").datepicker(
                {autoClose: true}
            );
        });

		var self = this
        reports=[]

        moment.locale('fr');

		this.on('mount', function() {
            var ajaxCall_customers = self.load_customers();
			ajaxCall_customers.done(function(data) {
				$(self.refs.customer_id).select2();
			})
            self.refs.day.value = moment().format('DD/MM/YYYY')
		});

        /******************************************
		load customers list
		*******************************************/

		load_customers(){
		var url = '/api/customers/';
		return $.ajax({
				url: url,
				type: "GET",
				dataType: "json",
				contentType: "application/json; charset=utf-8",
				success: function(data) {
					self.customers = data['customers']
					self.update()
				}
			});
		}
        search_reports(){
            var url = '/api/reports/shipments/'
            
            var customer_id = self.refs.customer_id.value;
            var period = self.refs.period.value;
            var day = self.refs.day.value;

            url = url.concat('period/',period,'/');
            url = url.concat('date/', day.replaceAll("/",""),'/');
            url = url.concat('customers/',customer_id);

            return $.ajax({
				url: url,
				type: "GET",
				dataType: "json",
				contentType: "application/json; charset=utf-8",
				success: function(data) {
					self.reports = data['reports']
					self.update()
				}
			});
            
        }

	</script>
</search-report-shipment>