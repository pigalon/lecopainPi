<search-subscription>
    <div class="form-group">
        <!--<input type="text"style="width:200px; display: inline-block;" name="day" ref="day" id="datepicker_day" data-language='fr' class="form-control datepicker-input" />
        <button type="button" id="search" onclick="{load_subscriptions}" class="btn btn-primary" ><i class="fa fa-search"></i></button>-->
        <input type="text" style="width:200px; display: inline-block;" name="month" ref="month" id="datepicker_day"  class="form-control datepicker-here" data-language='fr'  data-min-view="months"  data-view="months" data-date-format="mm/yyyy" />
        <button type="button" style="display: inline-block;" ref="search" name="search" id="search" onclick="{load_subscriptions}" class="btn btn-primary" ><i class="fa fa-search"></i></button>
        <b><span style="font-size:20px;"> &nbsp; &nbsp; &nbsp; Sélection du mois : {monthTitle}</span></b>
    </div>
    <table id="subscriptions_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="34%">Période</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ subscription in subscriptions }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_subscription(subscription.id) }>
                <tr>
                    <td onmouseover="changeBackgroundColor(this)" onmouseout="restoreBackgroundColor(this)" style="cursor: pointer" if={subscription.status == 'CREE'} width="6%" class="table-primary">{subscription.id} <span class="badge badge-warning" style="font-size:16px;">Ab.</span></td>
                    <td width="34%">du <b>{moment(subscription.start_dt).format('ddd Do MMM' )}</b> au <b>{moment(subscription.end_dt).format('ddd Do MMM YY' )}</b></td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_subscriptions_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> Abonnements précédents </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_subscriptions_next}"  style="color:white" class="btn btn-primary display:inline-block"> Abonnements suivants <i class="fas fa-arrow-right"></i> </a>
            </td>
            <td width="26%"> </td>
        </tr>
    </table>
    <br>
    <br>
    <script>

		var self = this
        var limit = 10
        var start= 1
        var next_url = ''
        var previous_url = ''

        moment.locale('fr');

		this.on('mount', function() {
            
            self.refs.month.value = moment().format('MM/YYYY')

            var dateMomentObject = moment('01/'+self.refs.month.value, "DD/MM/YYYY");
            
            monthTitle = moment(dateMomentObject).format('MMMM').charAt(0).toUpperCase() + moment(dateMomentObject).format('MMMM').slice(1)
            
            const location  = $('window.location')

            this.load_subscriptions()

		});

        $(function () {
            $("#datepicker_day").datepicker(
                {autoClose: true}
                
            );
        });

		/******************************************/
       	// load subscription list
    	/*******************************************/
		load_subscriptions(){
            var subscription_url = '/api/customer/subscriptions/';
            var period = 'month';

            var day = "01/"+self.refs.month.value;
            var date = moment(day).format('DD/MM/YYYY');
            monthTitle = moment(date).format('MMMM').charAt(0).toUpperCase() + moment(date).format('MMMM').slice(1)
            if (period == undefined){
                period = 'all'
            }

            subscription_url = subscription_url.concat('period/',period,'/');
            subscription_url = subscription_url.concat('date/', day.replaceAll("/",""));
        
            localStorage.setItem('search_subscription_url', subscription_url);

			this.load_subscriptions_from_url(subscription_url)
		}
        
        load_subscriptions_from_url(subscription_url){

			$.ajax({
                url: subscription_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
					self.subscriptions = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_subscriptions_next(){
            var subscription_url = self.next_url;
            localStorage.setItem('search_subscription_url', subscription_url);

			$.ajax({
                url: subscription_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.subscriptions = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_subscriptions_previous(){
            var subscription_url = self.previous_url;
            localStorage.setItem('search_subscription_url', subscription_url);

			$.ajax({
                url: subscription_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.subscriptions = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        show_subscription(subscription_id){
            return function(e) {
                location = "/customer/subscriptions/"+subscription_id;
            }
		}

	</script>
</search-subscription>