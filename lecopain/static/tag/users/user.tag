<search-user>
    <div class="form-group">
        Roles:
        <br>
        <select onchange={ load_users } class="form-control" name="role" id="role" ref="role" style="width: 12rem; display:inline-block" >
            <option value="0" SELECTED>Tous</option>
            <option each="{ role in roles }" value={role.id}>{role.name} </option>
        </select>
        <select class="form-control" id="user_id" name="user_id" ref="user_id" style="width: 12rem; display:inline-block">
            <option value="0" SELECTED>Tous</option>
            <option each="{ user_name in user_names }" value={user_name.id}> {user_name.username} </option>
        </select>
        <button type="button" id="search" onclick="{load_users}" class="btn btn-primary" ><i class="fa fa-search"></i></button>

        <div class="right">
            <a role="button" href="/users/new" class="btn btn-primary display:inline-block">Ajouter</i></a>
        </div>
    </div>
    <table id="users_list" width="100%">
        <tr>
            <td>
            <table width="100%">
                <tr>
                    <th width="6%">id</th>
                    <th width="20%">Login</th>
                    <th width="24%">Prénom Nom</th>
                    <th width="20%">Role</th>
                    <th width="10%">id Compte</th>
                    <th width="10%">Actif</th>
                </tr>
            </table>
            </td>
        </tr>
        <tr each="{ user in users }">
            <td>
            <table width="100%" class="table table-striped" onclick={ show_user(user.id) }>
                <tr>
                    <td width="6%" class="table-primary">{user.id}</td>
                    <td width="20%">{user.username}</td>
                    <td width="24%">{user.firstname} {user.lastname}</td>
                    <td width="20%">{user.role_name}</td>
                    <td width="10%">{user.account_id}</td>
                    <td width="10%">{user.active}</td>
                </tr>
            </table>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>
            <td width="24%"> </td>
            <td width="24%">
                <a if={ previous_url != '' && previous_url != undefined} role="button" onclick="{load_users_previous}"  style="color:white" class="btn btn-primary display:inline-block"> <i class="fas fa-arrow-left"></i> précédents </a>
            </td>
            <td width="2%">
                |
            </td>
            <td width="22%">
                <a if={ next_url != '' && next_url != undefined} role="button" onclick="{load_users_next}"  style="color:white" class="btn btn-primary display:inline-block"> suivants <i class="fas fa-arrow-right"></i> </a>
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
            
            var ajaxCall_roles = self.load_roles();
			ajaxCall_roles.done(function(data) {
				$(self.refs.role).select2();
			})

            var ajaxCall_user_names = self.load_user_names();
			ajaxCall_user_names.done(function(data) {
				$(self.refs.user_id).select2();
			})
            
            const location  = $('window.location')
		});

		/******************************************/
       	// load products list
        /*******************************************/
		load_users(){
            var user_url = '/api/users/';
            var role = self.refs.role.value;
            var user_id = self.refs.user_id.value;

            if (role == undefined){
                role = 'all'
            }

            user_url = user_url.concat('roles/',role);

            if ( user_id != undefined && user_id != '0'){
                user_url = user_url.concat('/id/',user_id);
            }

			$.ajax({
					url: user_url,
					type: "GET",
					dataType: "json",
					contentType: "application/json; charset=utf-8",
					success: function(data) {
						self.users = data['results']
                        self.count = data['count']
                        self.per_page = data['per_page']
                        self.page = data['page']
                        self.next_url = data['next']
                        self.previous_url = data['previous']
                        self.update()
					}
				});
		}
        load_users_next(){
            var user_url = self.next_url;

			$.ajax({
                url: user_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.users = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
                    self.update()
                }
            });
		}
        load_users_previous(){
            var user_url = self.previous_url;

			$.ajax({
                url: user_url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.users = data['results']
                    self.count = data['count']
                    self.per_page = data['per_page']
                    self.page = data['page']
                    self.next_url = data['next']
                    self.previous_url = data['previous']
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
        load_user_names(){
			var url = '/api/users/';
			return $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    self.user_names = data['users']
                    self.update()
                }
            });
		}
        show_user(user_id){
            return function(e) {
                console.log('show' + user_id)
                location = "/users/"+user_id;
            }
		}

	</script>
</search-user>