<search-shipment>
  <div class="form-group">
    <input type="text" style="width:200px; display: inline-block;" name="month" ref="month" id="datepicker_day"  class="form-control datepicker-here" data-language='fr'  data-min-view="months"  data-view="months" data-date-format="mm/yyyy" />
    <button type="button" style="display: inline-block;" ref="search" name="search" id="search" onclick="{load_shipments}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
    <b><span style="font-size:20px;"> &nbsp; &nbsp; &nbsp; Sélection du mois : {monthTitle} {yearTitle}</span></b>
  </div>

  <nav class="navbar navbar-light bg-light right">
    <form class="form-inline">
      <label id="nocanceled" class="switch" title="masquer annulations">
        <input onclick={ load_shipments } type="checkbox" id="check_nocanceled" ref="nocanceled" title="masquer annulations">
        <span class="slider round"></span>
      </label>
      <label id="nopaid" class="switch" title="masquer payés">
        <input onclick={ load_shipments } type="checkbox" id="check_nopaid" ref="nopaid"  title="masquer payées">
        <span class="slider round"></span>
      </label>
      <button class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#paymentModal">Payer Liste</button>
      <button class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#undoModal">Rétablir Liste</button>
      <button class="btn btn-sm btn-outline-secondary" type="button" style="float: right;" data-toggle="modal" data-target="#cancelModal">Annulation Liste</button>
      <a role="button" href="/shipments/new?customer_id={customer_id }" class="btn btn-sm btn-outline-secondary display:inline-block">Ajouter</a>
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
          <th width="2%"><input  type="checkbox" id="checkAll" name="checkAll"></th>
        </tr>
      </table>
      </td>
    </tr>
    <tr each="{ shipment in shipments }">
      <td>
        <table width="100%" class="table table-striped">
          <tr>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.updated_at == None && shipment.payment_status == 'NON'} width="6%" class="table-primary">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.updated_at != None && shipment.payment_status == 'NON'} width="6%" class="table-warning">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'CREE' && shipment.payment_status == 'OUI'} width="6%" class="table-success">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'ANNULEE'} width="6%" class="table-dark">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'TERMINEE'} width="6%" class="table-success">{shipment.id}</td>
            <td onclick={ show_shipment(shipment.id) } if={shipment.status == 'DEFAUT'} width="6%" class="table-danger">{shipment.id}</td>

            
            <td width="30%">{moment(shipment.shipping_dt).format('ddd Do MMM' )}</td>
            
            <td widht="10%">x{shipment.nb_products}</td>

            <td if={shipment.status == 'ANNULEE' && shipment.subscription_id == None} width="10%" >0.00 € </td>
            <td if={shipment.status != 'ANNULEE' && shipment.subscription_id == None} width="10%">
                {shipment.shipping_price.toFixed(2)} €
            </td>

            <td if={shipment.subscription_id != None} width="10%">
                <span nmouseover="" onclick={ show_subscription(shipment.subscription_id) } class="badge badge-warning" style="cursor: pointer;font-size:16px;">Ab.</span>
            </td>
            <td width="2%">
                <input class="check_list" onclick={ check_shipment } type="checkbox" ref="ids_{shipment.id}" id="ids_{shipment.id}" name="ids_{shipment.id}">
            </td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <table width="100%" >
        <tr class="bg-warning">
          <td width="10%">
          </td>
          <td width="30%">
          </td>
          <td width="10%">
          </td>
          <td width="10%">
            = {shipping_sum.toFixed(2)} €
          </td>
          <td width="2%">
          </td>
        </tr>
      </table>
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

  <div class="modal fade" id="paymentModal" ref="paymentModal" tabindex="-1" role="dialog" aria-labelledby="paymentModalLabel" aria-hidden="true">
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

  <div class="modal fade" id="cancelModal" ref="cancelModal" role="dialog" aria-labelledby="cancelModalLabel" aria-hidden="true">
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

    shipping_sum = 0.0
    this.selected_shipments = []
    this.id_shipments = []

    customer_id = opts.customer_id
    moment.locale('fr');

    /******************************************/
    //      RiotJS : Mount               
    /******************************************/
    this.on('mount', function() {

      const location  = $('window.location')
      self.refs.month.value = moment().format('MM/YYYY')

      var dateMomentObject = moment('01/'+self.refs.month.value, "DD/MM/YYYY");
      
      monthTitle = localStorage.getItem('search_customers_shipment_month');
      yearTitle = localStorage.getItem('search_customers_shipment_year');

      search_url = localStorage.getItem('search_customers_shipment_url');
      if(search_url != null){
        this.load_shipments_from_url(search_url)
      }
      else{
        this.load_shipments()
      }
    });

    /******************************************/
    //      JS : functions
    /******************************************/
    $(function () {
      $("#datepicker_day").datepicker(
          {autoClose: true}
      );
      $("#checkAll").click(function () {
        $('input:checkbox').not(this).filter('.check_list').prop('checked', this.checked);
        var inputs = document.getElementsByTagName("input");
        var checkbox = document.getElementById("checkAll");
        for(var i = 0; i < inputs.length; i++) {
          if(inputs[i].type == "checkbox" && inputs[i].id != 'check_nocanceled' && inputs[i].id != "check_nopaid") {
            if (checkbox.checked == true){
              self.add_one_in_checked_list(inputs[i].id);
            }
            else{
              self.remove_one_in_checked_list(inputs[i].id);
            }
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
      var shipment_url = '/api/shipments/customers/'+customer_id+'/';
      var period = 'month';

      var day = "01/"+self.refs.month.value;
      var date = moment(day).format('DD/MM/YYYY');
      monthTitle = moment(date).format('MMMM').charAt(0).toUpperCase() + moment(date).format('MMMM').slice(1)
      yearTitle = moment(date).format('YYYY').charAt(0).toUpperCase() + moment(date).format('YYYY').slice(1)
      
      if (period == undefined){
          period = 'all'
      }

      shipment_url = shipment_url.concat('period/',period,'/');
      shipment_url = shipment_url.concat('date/', day.replaceAll("/",""));

      localStorage.setItem('search_customers_shipment_url', shipment_url);
      localStorage.setItem('search_customers_shipment_month', monthTitle);
      localStorage.setItem('search_customers_shipment_year', yearTitle);

      this.load_shipments_from_url(shipment_url);

      if(self.refs.nocanceled.checked){
        shipment_url = shipment_url.concat('/nocanceled');
      }

      if(self.refs.nopaid.checked){
        shipment_url = shipment_url.concat('/nopaid');
      }
      return $.ajax({
        url: shipment_url,
        type: "GET",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function(data) {
          self.shipments = data['shipments']
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
    /******************************************/
    // load shipments from url
    /*******************************************/
    load_shipments_from_url(shipment_url){
			$.ajax({
        url: shipment_url,
        type: "GET",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function(data) {
          self.shipments = data['shipments']
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
    /**
      Check shipment
    **/
    check_shipment(e){
      console.log("check one id : ")
      if ($('#ids_'+e.item.shipment.id).is(':checked')) {
        console.log('push : ' + e.item.shipment.id)
        this.selected_shipments.push(e.item.shipment.id)
      }
      else{
        console.log("else check one id : " + e.item.shipment.id)
        for( var i = 0; i < this.selected_shipments.length; i++)
        { 
          if ( this.selected_shipments[i] === e.item.shipment.id) { 
            this.selected_shipments.splice(i, 1); 
          }
        }
      }
      console.log("this.selected_shipments : "+this.selected_shipments)
    }
    add_one_in_checked_list(id){
      idOnly = id.substring(4, id.length);
      console.log("id : " + idOnly)
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

    remove_one_in_checked_list(id){
      idOnly = id.substring(4, id.length);
      if (id != 'checkAll' && $('#'+id).is(':checked')) {
        this.selected_shipments.pop(idOnly)
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