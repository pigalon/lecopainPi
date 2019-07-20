<mytag>
	<h1> {orders_count_val}</h1>

	<script>
		this.val = 5;
		var self = this
		this.orders_count_val = 0;

		var url = 'https://localhost:5000/_getjs_order_count/'; //random adress
      	$.ajax({
            url: url,
            type: "GET",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(data) {
              self.orders_count_val = data['orders_count']
              self.update(this.orders_count_val)
            }
        });

	</script>
</mytag>