<search-shipment>

    <div class="form-group">
        <select class="form-control" name="customer_id" id="customer_id" ref="customer_id" style="width: 12rem; display:inline-block  z-index: 1; " >
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
        <button type="button" ref="search" name="search" id="search" onclick="{load_shipments}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
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
          <button class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#paymentModal">Payer Liste</button>
          <button class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#undoModal">Rétablir Liste</button>
          <button class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#cancelModal">Annulation Liste</button>
          <a role="button" href="/shipments/new" class="btn btn-sm btn-outline-secondary display:inline-block">Ajouter</a>
        </form>
    </nav>
    <table id="shipments_list" width="100%">
      <tr>
        <td>
        <table id="table_title_mobile" width="100%">
          <tr>
            <th width="6%">id</th>
            <th width="20%">Date</th>
            <th width="30%">Client</th>
            <th width="10%">Liv.</th>
          </tr>
        </table>
        <table id="table_title_site" width="100%">
          <tr>
            <th width="6%">id</th>
            <th width="20%">Date</th>
            <th width="30%">Client</th>
            <th width="10%">Liv.</th>
            <th width="2%"><input  type="checkbox" id="checkAll" name="checkAll"></th>
          </tr>
        </table>
        </td>
      </tr>
      <tr each="{ shipment in shipments }">
        <td>
        <table id="table_mobile" width="100%" class="table table-striped">
          <tr>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.updated_at == None && shipment.payment_status == 'NON'} width="6%" class="table-primary">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.updated_at != None && shipment.payment_status == 'NON'} width="6%" class="table-warning">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.payment_status == 'OUI'} width="6%" class="table-success">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'ANNULEE'} width="6%" class="table-dark">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'TERMINEE'} width="6%" class="table-success">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'DEFAUT'} width="6%" class="table-danger">{shipment.id}</td>

            <td width="20%">{moment(shipment.shipping_dt).format('ddd Do MMM' )}</td>
            <td width="30%"><a onclick={ show_customer(shipment.customer_id) }>{shipment.customer_name}</a></td>
            <td if={shipment.status == 'ANNULEE'} width="10%" >0.00 € <br><span onclick={ show_subscription(shipment.subscription_id) } if={shipment.subscription_id != None} class="badge badge-warning" style="font-size:16px;">Ab.</span></td>
            <td if={shipment.status != 'ANNULEE'} width="10%">
              {shipment.shipping_price.toFixed(2)} € <br><span onclick={ show_subscription(shipment.subscription_id) } if={shipment.subscription_id != None} class="badge badge-warning" style="font-size:16px;">Ab.</span>
            </td>
          </tr>
        </table>
        <table id="table_site" width="100%" class="table table-striped">
          <tr>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.updated_at == None && shipment.payment_status == 'NON'} width="6%" class="table-primary">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.updated_at != None && shipment.payment_status == 'NON'} width="6%" class="table-warning">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.payment_status == 'OUI'} width="6%" class="table-success">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'ANNULEE'} width="6%" class="table-dark">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'TERMINEE'} width="6%" class="table-success">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'DEFAUT'} width="6%" class="table-danger">{shipment.id}</td>

            <td width="20%">{moment(shipment.shipping_dt).format('ddd Do MMM' )}</td>
            <td width="30%"><span onclick={ show_customer(shipment.customer_id) } class="badge badge-primary" style="font-size:14px;"><i class="fas fa-user"></i></span> {shipment.customer_name}</td>
            <td if={shipment.status == 'ANNULEE'} width="10%" >0.00 € <br><span onclick={ show_subscription(shipment.subscription_id) } if={shipment.subscription_id != None} class="badge badge-warning" style="font-size:16px;">Ab.</span></td>
            <td if={shipment.status != 'ANNULEE'} width="10%">
              {shipment.shipping_price.toFixed(2)} € <br><span onclick={ show_subscription(shipment.subscription_id) } if={shipment.subscription_id != None} class="badge badge-warning" style="font-size:16px;">Ab.</span>
            </td>
            <td width="2%">
              <input class="check_list" onclick={ check_shipment } onchange={ check_shipment } type="checkbox" ref="ids_{shipment.id}" id="ids_{shipment.id}" name="ids_{shipment.id}">
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
          <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_shipments_previous}"  style="color:white" class="btn btn-sm btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Précédent </a>
        </td>
        <td width="2%">
          |
        </td>
        <td width="22%">
          <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_shipments_next}"  style="color:white" class="btn btn-sm btn-primary display:inline-block"> Suivant <i class="fas fa-arrow-right"></i> </a>
        </td>
        <td width="26%"> </td>
      </tr>
    </table>
    
    <br>
    <br>

    <div class="modal fade" id="paymentModal" tabindex="-1" role="dialog" aria-labelledby="paymentModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="paymentModalLabel">P</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          Etes-vous sur de passer à "payé" les livraisons sélectionnées"  ?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Fermer</button>
          <button onclick={pay_list} type="button" class="btn btn-primary" id="ok_pay" name="ok_pay">Confirmer</button>
        </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="cancelModal" ref="cancelModal" tabindex="-1" role="dialog" aria-labelledby="cancelModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Annulation</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            Etes-vous sur d'annuler les livraisons sélectionnées?
          </div>
          <div class="modal-footer">
            <button  type="button" class="btn btn-secondary" data-dismiss="modal">Fermer</button>
            <button onclick={cancel_list} type="button" class="btn btn-primary" id="ok_cancel" name="ok_cancel">Confirmer</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="undoModal" ref="undoModal" tabindex="-1" role="dialog" aria-labelledby="undoModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Rétablir</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            Etes-vous sûr de vouloir rétablir les livraisons sélectionnées?
          </div>
          <div class="modal-footer">
            <button  type="button" class="btn btn-secondary" data-dismiss="modal">Fermer</button>
            <button onclick={undo_list} type="button" class="btn btn-primary" id="ok_undo" name="ok_undo">Confirmer</button>
          </div>
        </div>
      </div>
    </div>

  <script>
		var self = this
    var per_page = 10
    var page= 1
    var next_url = ''
    var previous_url = ''
    var customer_id='0';

    this.selected_shipments = []
    this.id_shipments = []

    moment.locale('fr');

		this.on('mount', function() {
			
      var ajaxCall_customers = self.load_customers();
			ajaxCall_customers.done(function(data) {
				$(self.refs.customer_id).select2();
			})
      const location  = $('window.location')
      self.refs.day.value = moment().format('DD/MM/YYYY')

      search_url = localStorage.getItem('search_shipment_url');
			if(search_url != null){
        this.load_shipments_from_url(search_url)
			}
      else{
        this.load_shipments()
      }

		});

    $(function () {
      $("#datepicker_day").datepicker(
        {autoClose: true}
      );

      $("#checkAll").click(function () {
        $('input:checkbox').not(this).filter('.check_list').prop('checked', this.checked);
        var inputs = document.getElementsByTagName("input");
        
        for(var i = 0; i < inputs.length; i++) {
          if(inputs[i].type == "checkbox" && inputs[i].id != 'check_nocanceled' && inputs[i].id != "check_nopaid" && inputs[i].checked) {
            self.add_one_in_checked_list(inputs[i].id);
          }
        }
      });

      $("#ok_cancel").click(function (){
        $('#cancelModal').modal('hide');
      });
      $("#ok_undo").click(function (){
        $('#undoModal').modal('hide');
      });
    });

		/******************************************/
    // load shipments list
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
      
      if(self.refs.nocanceled.checked){
        shipment_url = shipment_url.concat('/nocanceled');
      }

      if(self.refs.nopaid.checked){
        shipment_url = shipment_url.concat('/nopaid');
      }

      localStorage.setItem('search_shipment_url', shipment_url);

      this.load_shipments_from_url(shipment_url);
		}
    /**
      Load shipment from url
    */
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
    /** 
      Load shipment next 
    **/
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
    /**
      Load shipment from previous
    **/
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
    /**
      Load Customers
    **/
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
  /**
    Show shipment
  **/
    show_shipment(shipment_id){
      return function(e) {
        location = "/shipments/"+shipment_id;
      }
		}
    /**
      Show subscription
    **/
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
    /**
      Check shipment
    **/
    check_shipment(e){
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
    /**
      add one item in checked list
    **/
    add_one_in_checked_list(id){
      idOnly = id.substring(4, id.length);
      if (id != 'checkAll' && $('#'+id).is(':checked')) {
        this.selected_shipments.push(idOnly)
      }
      else{
        for( var i = 0; i < this.selected_shipments.length; i++)
        { 
          if ( this.selected_shipments[i] === idOnly) { 
            this.selected_shipments.splice(i, 1); 
          }
        }
      }
    }
    
    /**
      Cancel list
    **/
    cancel_list(){
      console.log('1' +  this.selected_shipments)
      this.selected_shipments.forEach(
        item => (this.id_shipments.push({"id" : item}))
      )
            
      if(this.id_shipments.length >0){
        console.log('3')
        var url = '/api/shipments/cancel/';
        var data = JSON.stringify(this.id_shipments);
        return $.ajax({
          url: url,
          data: data,
          type: "POST",
          dataType: "json",
          contentType: "application/json; charset=utf-8",
          success: function(data) {
            location.reload();
            console.log('4')
            self.update();
          }
        });
      }
    }
    /**
      Pay list
    **/
    pay_list(){
      this.selected_shipments.forEach(
        item => (this.id_shipments.push({"id" : item}))
      )      
      if(this.id_shipments.length >0){
        var url = '/api/shipments/pay/';
        var data = JSON.stringify(this.id_shipments);
        return $.ajax({
          url: url,
          data: data,
          type: "POST",
          dataType: "json",
          contentType: "application/json; charset=utf-8",
          success: function(data) {
            location.reload(); 
            self.update();
          }
        });
      }
    }
    /**
      Undo list
    **/
    undo_list(){
      this.selected_shipments.forEach(
        item => (this.id_shipments.push({"id" : item}))
      )      
      if(this.id_shipments.length >0){
        var url = '/api/shipments/undo/';
        var data = JSON.stringify(this.id_shipments);
        return $.ajax({
          url: url,
          type: "POST",
          dataType: "json",
          data: data,
          contentType: "application/json; charset=utf-8",
          success: function(data) {
            location.reload(); 
            self.update();
          }
        });
      }
    }

	</script>
</search-shipment>