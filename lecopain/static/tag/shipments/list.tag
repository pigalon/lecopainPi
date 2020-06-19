<search-shipment>
    <div class="form-group">
        <select class="form-control" name="customer_id" id="customer_id" ref="customer_id" style="width: 12rem; display:inline-block" >
            <option value="0" SELECTED>Tous</option>
            <option each="{ customer in customers }" value={customer.id}>{customer.firstname} {customer.lastname}</option>
        </select>
        <input type="text"style="width:200px; display: inline-block;" name="day" ref="day" id="datepicker_day" data-language='fr' class="form-control datepicker-input" />
        <select class="form-control" name="period" id="period" ref="period" style="width: 12rem; display:inline-block">
            <option value="day">Jour</option>
            <option value="week">Semaine</option>
            <option value="month">Mois</option>
            <option value="all">Toutes</option>
        </select>
        <button type="button" id="search" onclick="{load_shipments}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
        <div class="right">
            <a role="button" href="/shipments/new" class="btn btn-primary display:inline-block">Ajouter</i></a>
        </div>
    </div>
    <table id="shipments_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="20%">date</th>
                    <th width="30%">client</th>
                    <th width="20%">Status</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ shipment in shipments }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_shipment(shipment.id) }>
                <tr>
                    <td if={shipment.status == 'CREE' && shipment.updated_at == None} width="6%" class="table-primary">{shipment.id}</td>
                    <td if={shipment.status == 'CREE' && shipment.updated_at != None} width="6%" class="table-warning">{shipment.id}</td>
                    <td if={shipment.status == 'ANNULEE'} width="6%" class="table-dark">{shipment.id}</td>
                    <td if={shipment.status == 'TERMINEE'} width="6%" class="table-success">{shipment.id}</td>
                    <td if={shipment.status == 'DEFAUT'} width="6%" class="table-danger">{shipment.id}</td>

                    <td width="20%">{moment(shipment.shipping_dt).format('ddd Do MMMM' )}</td>
                    <td width="30%">{shipment.customer_name}</td>
                    <td width="20%"><span if={shipment.shipping_status == 'OUI'} style="color:green" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={shipment.shipping_status == 'NON'} style="color:grey" ><i class="fas fa-cart-arrow-down "></i></span>
                    <span if={shipment.payment_status == 'OUI'} style="color:green" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={shipment.payment_status == 'NON'} style="color:grey" ><i class="fas fa-credit-card"></i></i></span>
                    <span if={shipment.subscription_id != None} class="badge badge-warning">Ab.</span>
                    </td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ (start - limit) > 0 } role="button" onclick="{load_shipments_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Livraisons précédentes </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ (start + limit) <= count } role="button" onclick="{load_shipments_next}"  style="color:white" class="btn btn-primary display:inline-block"> Livraisons suivantes <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>
    <br>
    <br>
    <script>
		var self = this
        var next_start = 0
        var previous_start = 0
        var limit = 10
        var start= 1
        var next_url = ''

        moment.locale('fr');

		this.on('mount', function() {
			this.load_shipments()
            
            var ajaxCall_customers = self.load_customers();
			ajaxCall_customers.done(function(data) {
				$(self.refs.customer_id).select2();
			})
            const location  = $('window.location')
            self.refs.day.value = moment().format('DD/MM/YYYY')
		});

        $(function () {
            $("#datepicker_day").datepicker(
                {autoClose: true}
                
            );
        });

        String.prototype.replaceAll = function(str1, str2, ignore)
		{
    		return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
		}

		/******************************************/
       	// load products list
    	/*******************************************/
		load_shipments(){
            var shipment_url = '/api/shipments/';
            var customer_id = self.refs.customer_id.value;
            var period = self.refs.period.value;

            var day = self.refs.day.value;

            
            
            if (period == undefined){
                period = 'all'
            }

            shipment_url = shipment_url.concat('period/',period,'/');
            shipment_url = shipment_url.concat('date/', day.replaceAll("/",""),'/');
            shipment_url = shipment_url.concat('customers/',customer_id);

			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.limit = data['limit']
                    self.start = data['start']
                    self.next_start = parseInt(data['start'])+parseInt(limit)
                    self.previous_start = parseInt(data['start'])-parseInt(limit)
                    self.next_url = data['next']
                    self.update()
                }
            });
		}
        load_shipments_next(){
            var shipment_url = self.next_url;

			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.limit = data['limit']
                    self.start = data['start']
                    self.next_start = parseInt(data['start'])+parseInt(limit)
                    self.previous_start = parseInt(data['start'])-parseInt(limit)
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_shipments_previous(){
            var shipment_url = self.previous_url;

			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.limit = data['limit']
                    self.start = data['start']
                    self.next_start = parseInt(data['start'])+parseInt(limit)
                    self.previous_start = parseInt(data['start'])-parseInt(limit)
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
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

        show_shipment(shipment_id){
            return function(e) {
                location = "/shipments/"+shipment_id;
            }
		}

	</script>
</search-shipment>