<search-shipment>
    <div class="form-group">
        <b><span style="font-size:20px;"> &nbsp; &nbsp; &nbsp; Abonnement N° {subscription.id} du <b>{moment(subscription.start_dt).format('ddd Do MMM' )}</b> au <b>{moment(subscription.end_dt).format('ddd Do MMM YY' )}</b>
        <label id="nocanceled" class="switch" title="masquer annulations">
          <input type="checkbox" id="check_nocanceled" ref="nocanceled" title="masquer annulations">
          <span class="slider round"></span>
        </label>
        <label id="nopaid" class="switch" title="masquer payés">
          <input type="checkbox" id="check_nopaid" ref="nopaid"  title="masquer payées">
          <span class="slider round"></span>
        </label>
    </div>
    <nav class="navbar navbar-light bg-light right">
      <form class="form-inline">
        <!--<button if={customer_id != undefined && customer_id.value != "0"} class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#modificationModal">Modification Liste</button>-->
        <button id="paymentModal" class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#paymentModal">Payer Liste</button>
        <button id="undoModal" class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#undoModal">Rétablir Liste</button>
        <button id="cancelModal" class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#cancelModal">Annulation Liste</button>
        <a role="button" href="/shipments/new" class="btn btn-sm btn-outline-secondary display:inline-block">Ajouter</a>
      </form>
    </nav>
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
                <td onmouseover="changeBackgroundColor(this)" onmouseout="restoreBackgroundColor(this)" style="cursor: pointer" onclick={ show_shipment(shipment.id) } width="6%" class="table-primary">
                  <i class="fas fa-cart-arrow-down "></i>{shipment.id}
                </td>
                <td width="30%">
                  {moment(shipment.shipping_dt).format('ddd Do MMM' )}
                </td>
                <td widht="10%">
                  x{shipment.nb_products}
                </td>
                <td if={shipment.status == 'ANNULEE' && shipment.subscription_id == None} width="10%">
                  0.00 €
                </td>
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
          <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_shipments_previous}"  style="color:white" class="btn btn-primary display:inline-block">
            <i class="fas fa-arrow-left"></i> Livraisons précédentes
          </a>
        </td>
        <td width="2%">
        </td>
        <td width="22%">
          <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_shipments_next}"  style="color:white" class="btn btn-primary display:inline-block">
            Livraisons suivantes
            <i class="fas fa-arrow-right"></i>
          </a>
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
      subscription_id =  opts.subscription_id

      this.selected_shipments = []

      customer_id = opts.customer_id
      moment.locale('fr');

      this.on('mount', function() {
            
            const location  = $('window.location')
            this.load_shipments(subscription_id);
      });

      $(function () {
          $("#datepicker_day").datepicker(
              {autoClose: true}
          );
      });

      /******************************************/
      // load shipments list
      /*******************************************/
      /******************************************/
       	// load products list
    	/*******************************************/
		load_shipments(subscription_id){
            var shipment_url = '/api/shipments/subscriptions/'+subscription_id;
            console.log('call load ship : '+ shipment_url)
			return $.ajax({
					url: shipment_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
            self.shipments = data['results']
            self.count = data['count']
            self.shipping_sum = 0.0
            self.shipments.forEach((shipment) => {
                if(shipment.status != 'ANNULEE'){
                    self.shipping_sum = shipment.shipping_price  + self.shipping_sum;
                }
            });
            self.update()
					}
				});
		}
      
    show_shipment(shipment_id){
      return function(e) {
          location = "/customer/shipments/"+shipment_id;
      }
		}
    show_subscription(subscription_id){
      return function(e) {
        location = "/customer/subscriptions/"+subscription_id;
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