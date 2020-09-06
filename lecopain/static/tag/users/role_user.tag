<role-user>
    <div class="card  " >
        <div class="card-header text-white bg-info">
           Utilisateur Choisi
        </div>
        <div class="card-body">
        <ul>
            <li>
                <b>Utilisateur</b> : {user.firstname} {user.lastname}
            </li>
            <li>
                <b>Role actuel de l'utilisateur</b> : {user.role_name}
            </li>
            <li>
                <b>Compte actuel de l'utilisateur</b> : {user.account_id} - {account_detail}
            </li>
        </ul>
        </div>
    </div>

    <div class="card  " >
        <div class="card-header text-white bg-info">
            Changement
        </div>
        <div class="card-body">
        <div class="form-group">
            Roles:
            <select class="form-control" name="role_id" id="role_id" ref="role_id" style="width: 12rem; display:inline-block" >
                <option value="0" SELECTED>Aucun</option>
                <option each="{ role in roles }" value={role.id}>{role.name}</option>
            </select>
            <br>
            <div ref='customer_block' id='customer_block'>
                Choix du compte d'un client :

                <select class="form-control" id="customer_id" name="customer_id" ref="customer_id" style="width: 12rem; display:inline-block">
                    <option value="0" SELECTED>Aucun</option>
                    <option each="{ customer_name in customer_names }" value={customer_name.id}> {customer_name.firstname} {customer_name.lastname}</option>
                </select>
                <br>
            </div>
            
            <div ref='seller_block' id='seller_block'>
                Choix du compte d'un vendeur :
                <select class="form-control" id="seller_id" name="seller_id" ref="seller_id" style="width: 12rem; display:inline-block">
                    <option value="0" SELECTED>Aucun</option>
                    <option each="{ seller_name in seller_names }" value={seller_name.id}> {seller_name.name} </option>
                </select>
            </div>
            <br>
            <button type="button" id="Change" onclick="{change_role}" class="btn btn-info" >Valider</button>
        
        </div>
        </div>
    </div>
    <script>

		var self = this

        _id =  opts._id
        user_id =  opts.user_id
        user = {'firstname':' ',
                'lastname':' ', 
                'role_name':' '}

        moment.locale('fr');

		this.on('mount', function() {

            firstname = ''
            lastname = ''
            role_name = ''
            account_id = ''
            account_detail = ''

            var ajaxCall_roles = self.load_roles();
			ajaxCall_roles.done(function(data) {
				$(self.refs.role_id).select2().on('change', self.role_selection);
			})

            var ajaxCall_customers = self.load_customer_names();
			ajaxCall_customers.done(function(data) {
				$(self.refs.customer_id).select2()
			})

            var ajaxCall_sellers = self.load_seller_names();
			ajaxCall_sellers.done(function(data) {
				$(self.refs.seller_id).select2();
			})

            var ajaxCall_user = self.load_user(user_id);
            ajaxCall_user.done(function(data) {

                role_id = parseInt(self.user.role_id);
                $(self.refs.role_id).select2().val(role_id);
                $(self.refs.role_id).select2().trigger('change');

                if (self.user.role_name == 'customer_role'){
                    $(self.refs.customer_id).select2().val(self.user.account_id);
                    $(self.refs.customer_id).select2().trigger('change');
                    self.load_account_customer(self.user.account_id)
                }
                if (self.user.role_name =='seller_role'){
                    $(self.refs.seller_id).select2().val(self.user.account_id);
                    $(self.refs.seller_id).select2().trigger('change');
                    self.load_account_seller(self.user.account_id)
                }
            })  

            const location  = $('window.location')
		});

		/******************************************/
       	// change role
        /*******************************************/
		change_role(){
            var user_url = '/api/users/update';
            var role_id = self.refs.role_id.value;

            var customer_id = self.refs.customer_id.value;
            var seller_id = self.refs.seller_id.value;
            var account_id = 0

            if (customer_id > 0){
                account_id = customer_id
            }
            else if (seller_id > 0){
                account_id = seller_id
            }

            user_url = user_url.concat('/', user_id);

            user_url = user_url.concat('/role/',role_id);

            user_url = user_url.concat('/account/',account_id);

			$.ajax({
                url: user_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.update()
                    location='/users/update/'+user_id+'/role'
                }
            });
		}
        role_selection(){
            var index = parseInt(self.refs.role_id.selectedIndex);
			text = this.refs.role_id[index].innerText;
            if(text == 'customer_role'){
                this.refs.seller_block.style.display = 'none';
                this.refs.customer_block.style.display = 'block';
            }
            else if(text == 'seller_role'){
                this.refs.seller_block.style.display = 'block';
                this.refs.customer_block.style.display = 'none';
            }
            else{
                this.refs.seller_block.style.display = 'none';
                this.refs.customer_block.style.display = 'none';
            }
        }
        load_account_customer(id){
			var url = '/api/customers/'+id;
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.account_detail = data['customer'].firstname + ' ' + data['customer'].lastname
                    self.update()
                }
            });
		}
        load_account_seller(id){
			var url = '/api/sellers/'+id;
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.account_detail = data['seller'].name
                    self.update()
                }
            });
		}
        load_customer_names(){
			var url = '/api/customers/';
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.customer_names = data['customers']
                    self.update()
                }
            });
		}
        load_seller_names(){
			var url = '/api/sellers/select';
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.seller_names = data['sellers']
                    self.update()
                }
            });
		}
        load_roles(){
			var url = '/api/users/roles';
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.roles = data['roles']
                    self.update()
                }
            });
		}
        load_user(user_id){
            var url = '/api/users/'+user_id;
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.user = data['user']
                    self.update()
                }
            });
        }
        load_customer(customer_id){
            var url = '/api/customers/'+customer_id;
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.customer = data['customer']
                    self.update()
                }
            });
        }
        load_seller(seller_id){
            var url = '/api/sellers/'+seller_id;
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.seller = data['seller']
                    self.update()
                }
            });
        }

	</script>
</role-user>