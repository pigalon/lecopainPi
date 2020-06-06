<search-report>
    <div class="form-group">
        <table id="orders_list" width="100%">
            <tr>
                <td>Vendeur :</td><td>Date</td><td>Durée</td><td></td>
            </tr>
            <tr>
                <td>
                    <select class="form-control" id="seller_id" name="seller_id" ref="seller">
					    <option each="{ seller in sellers }" value={seller.id}> {seller.name} </option>
                    </select>
                </td>
                <td>
                    <input type="text" name="day" id="datepicker_day" data-language='fr' class="form-control datepicker-input" />
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
        <p>
        { result }
        </p>

    <script>

         $(function () {
            $("#datepicker_day").datepicker();
        });

		var self = this

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

        search(){
            result = " un Début !!"
            self.update()
        }

	</script>
</search-report>