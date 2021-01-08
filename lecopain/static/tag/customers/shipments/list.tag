<search-shipment>
    <div class="form-group">
        <input type="text" style="width:200px; display: inline-block;" name="month" ref="month" id="datepicker_day"  class="form-control datepicker-here" data-language='fr'  data-min-view="months"  data-view="months" data-date-format="mm/yyyy" />
        <button type="button" style="display: inline-block;" ref="search" name="search" id="search" onclick="{load_shipments}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
        <b><span style="font-size:20px;"> &nbsp; &nbsp; &nbsp; Sélection du mois : {monthTitle}</span></b>
    </div>
    
    <table id="shipments_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">N°</th>
                    <th width="30%">Date</th>
                    <th widht="10%">Nb Articles</th>
                    <th width="10%">Liv.</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ shipment in shipments }">
            <td>
            
            <table width="100%" class="table table-striped">
                <tr>
                    <td onmouseover="changeBackgroundColor(this)" onmouseout="restoreBackgroundColor(this)" style="cursor: pointer" onclick={ show_shipment(shipment.id) } width="6%" class="table-primary"><i class="fas fa-cart-arrow-down "></i>{shipment.id}</td>
                    
                    <td width="30%">{moment(shipment.shipping_dt).format('ddd Do MMM' )}</td>
                    
                    <td widht="10%">x{shipment.nb_products}</td>

                    <td if={shipment.status == 'ANNULEE' && shipment.subscription_id == None} width="10%" >0.00 € </td>
                    <td if={shipment.status != 'ANNULEE' && shipment.subscription_id == None} width="10%">
                        {shipment.shipping_price.toFixed(2)} €
                    </td>

                    <td if={shipment.subscription_id != None} width="10%">
                        <span nmouseover="" onclick={ show_subscription(shipment.subscription_id) } class="badge badge-warning" style="cursor: pointer;font-size:16px;">Ab.</span>
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
                <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_shipments_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Livraisons précédentes </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_shipments_next}"  style="color:white" class="btn btn-primary display:inline-block"> Livraisons suivantes <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>

    <br>
    <br>
    <script>
		var self = this
        var per_page = 10
        var page= 1
        var next_url = ''
        var previous_url = ''

        this.selected_shipments = []

        customer_id = opts.customer_id
        moment.locale('fr');

		this.on('mount', function() {
            
            const location  = $('window.location')
            self.refs.month.value = moment().format('MM/YYYY')

            var dateMomentObject = moment('01/'+self.refs.month.value, "DD/MM/YYYY");
            
            monthTitle = moment(dateMomentObject).format('MMMM').charAt(0).toUpperCase() + moment(dateMomentObject).format('MMMM').slice(1)

            this.load_shipments()

		});

        $(function () {
            $("#datepicker_day").datepicker(
                {autoClose: true}
            );
        });

		/******************************************/
       	// load shipments list
    	/*******************************************/
		load_shipments(){
            var shipment_url = '/api/shipments/customers/'+customer_id+'/';
            var period = 'month';

            var day = "01/"+self.refs.month.value;
            var date = moment(day).format('DD/MM/YYYY');
            monthTitle = moment(date).format('MMMM').charAt(0).toUpperCase() + moment(date).format('MMMM').slice(1)
            
            if (period == undefined){
                period = 'all'
            }

            shipment_url = shipment_url.concat('period/',period,'/');
            shipment_url = shipment_url.concat('date/', day.replaceAll("/",""));

            localStorage.setItem('search_shipment_url', shipment_url);

            this.load_shipments_from_url(shipment_url);

		}
        load_shipments_from_url(shipment_url){

			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_shipments_next(){
            var shipment_url = self.next_url;
            localStorage.setItem('search_shipment_url', shipment_url);
			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_shipments_previous(){
            var shipment_url = self.previous_url;
            localStorage.setItem('search_shipment_url', shipment_url);
			$.ajax({
                url: shipment_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.shipments = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}

        show_shipment(shipment_id){
            return function(e) {
                location = "/shipments/"+shipment_id;
            }
		}
        show_subscription(subscription_id){
            return function(e) {
                location = "/subscriptions/"+subscription_id;
            }
		}
        show_customer(customer_id){
            return function(e) {
                location = "/customers/"+customer_id;
            }
		}

        check_shipement(e){
            if ($('#ids_'+e.item.shipment.id).is(':checked')) {
                this.selected_shipments.push(e.item.shipment.id)
            }
            else{
                for( var i = 0; i < this.selected_shipments.length; i++)
                { 
                    if ( this.selected_shipments[i] === e.item.shipment.id) { 
                        this.selected_shipments.splice(i, 1); 
                    }
                }
            }
        }

        cancel_list(){
            var str_shipment_ids = ''
            this.selected_shipments.forEach(
                item => (str_shipment_ids = str_shipment_ids.concat(item,','))
                )
            var url = '/api/shipments/cancel/ids/'+str_shipment_ids;
            return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    location.reload(); 
                    self.update()
                }
            });
		}

	</script>
</search-shipment>