<mytag>
	<h1> {total_orders_count_val} {in_progress_orders_count_val} </h1>

	<script>
		this.val = 5;
		var self = this
		this.total_orders_count_val = 0;
		this.in_progress_orders_count_val = 0;

		var url = 'https://localhost:5000/_getjs_order_count/'; //random adress
      	$.ajax({
            url: url,
            type: "GET",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(data) {
              self.total_orders_count_val = data['total_orders_count']
              self.in_progress_orders_count_val = data['in_progress_orders_count']

              self.update(this.in_progress_orders_count_val)
              self.update(this.in_progress_orders_count_val)
            }
        });

	</script>
</mytag>