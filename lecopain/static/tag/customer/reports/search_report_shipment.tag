<search-report-shipment>
    <div class="form-group">
        Client:
        <br>
        <input type="text" style="width: 12rem; display:inline-block" name="day" ref="day" id="datepicker_day" data-language='fr' class="form-control datepicker-input" />
        <select class="form-control" name="period" id="period" ref="period" style="width: 12rem; display:inline-block">
            <option value="day">Jour</option>
            <option value="week">Semaine</option>
            <option value="month">Mois</option>
        </select>
        <button type="button" id="search" onclick="{search_reports}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
        <br>
        
    </div>

    <h4>Total Période</h4> 
    <ul>
        <li><b>Nb Livraisons</b> : <span class="btn btn-warning">x{reports['nb_shipments']}</span> </li>
        <li><b>Nb Articles</b> : <span class="btn btn-warning">x{reports['nb_products']}</span></li>  
        <li><b>Montant Livraison total</b> : <span class="btn btn-warning">{reports['shipping_price']} €</span></li>
    </ul>
        <br><br>
        <h4>Liste des livraisons:</h4> 
        <br>
        <table class="table table-bordered table-striped">
            <thead>
                <th>
                    Date
                </th>
                <th>
                    N° de Livraison
                </th>
                <th>
                    Client
                </th>
                <th>
                    Montant
                </th>
                <th>
                    Informations
                </th>
            </thead>
            <tr each="{shipment in reports['shipments']}">
                <td>
                    {moment(shipment.shipping_dt).format('ddd Do MMMM' )}
                </td>
                <td>
                    {shipment.id}
                </td>
                <td>
                    {shipment.customer_name}
                </td>
                <td>
                    {shipment.shipping_price.toFixed(2)} €
                </td>
                <td>
                    <span if={shipment.subscription_id != None} class="badge badge-warning">Ab.</span>
                </td>
            </tr>
        </table>
    <script>

        $(function () {
            $("#datepicker_day").datepicker(
                {autoClose: true}
            );
        });

		var self = this
        reports=[]

        moment.locale('fr');

		this.on('mount', function() {
            self.refs.day.value = moment().format('DD/MM/YYYY')
		});

        
        search_reports(){
            var url = '/api/customer/reports/shipments/'
            
            var period = self.refs.period.value;
            var day = self.refs.day.value;

            url = url.concat('period/',period,'/');
            url = url.concat('date/', day.replaceAll("/",""));

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