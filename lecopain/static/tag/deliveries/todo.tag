
<todo>

  <h3>{ opts.title }</h3>

  <ul>
    <li each={ items.filter(whatShow) }>
      <label class={ completed: done }>
        <input type="checkbox" checked={ done } onclick={ parent.toggle }> { name }
      </label>
    </li>
  </ul>


  <form onsubmit={ allTodos}>
    <input ref="input" onkeyup={ edit }>
    <button disabled={ !text }>Add #{ items.filter(whatShow).length + 1 }</button>

    <button type="button" disabled={ items.filter(onlyDone).length == 0 } onclick={ removeAllDone }>
    X{ items.filter(onlyDone).length } </button>
  </form>


  <table>
  <tr>
  <td>
  <select class="form-control" ref="vendor" width="300px" onchange={ load_products }>
    <option each="{ vendor in vendors }" value={vendor.id}> {vendor.name} </option> 
  </select>
  </td>
  <td>
  <select class="form-control" ref="product" width="300px">
    <option each="{ product in products }" value={product.id}> {product.name} </option> 
  </select>
  </td>
  <td>
    <button type="button"  onclick={ addProduct }>ADD</button>
  </td>
  </tr>
  </table>

  <ul>
    <li each={ selected_products.filter(whatShow) }>
      <label class={ completed: done }>
        <input type="checkbox" checked={ done } onclick={ parent.toggle }> { id } - { name }
      </label>
    </li>
  </ul>






  <!-- this script tag is optional -->
  <script>

    var self = this

    this.items = opts.items
    this.selected_products = opts.selected_products

    this.vendors = []
    this.products = []

    this.on('mount', function(){

      self.load_vendors()
  
    })



    load_vendors(){
      var url = 'http://localhost:5000/_getjs_vendors/'; //random adress
      $.ajax({
            url: url,
            type: "GET",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(data) {
              self.vendors = data['vendors']
              self.update()
            }
        });
    }
    
    load_products(){
        vendor_id = this.refs.vendor.value
        var url = 'http://localhost:5000/_getjs_products/'+vendor_id;
      $.ajax({
            url: url,
            type: "GET",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(data) {
              self.products = data['products']
              self.update()
            }
        });
    }
    addProduct(e){
      
      product_id = this.refs.product.value
      product_name = this.refs.product[product_id].text
      

      console.log('product_id : ' + product_id + ' - ' + product_name)

      if (product_name) {
        this.selected_products.push({ id : product_id, name: product_name })
        this.text = this.refs.input.value = ''
      }
      e.preventDefault()


    }

    /*allTodos(){
      
      var test = [{done:'true', due_date:'11', title:'the title'}, {done:'true', due_date:'11', title:'the title'}]
      return test
    }*/

   /* await mount_vendors(){

    }*/

    edit(e) {
      this.text = e.target.value
    }

    add(e) {
      if (this.text) {
        this.items.push({ name: this.text })
        this.text = this.refs.input.value = ''
      }
      e.preventDefault()
    }

    removeAllDone(e) {
      this.items = this.items.filter(function(item) {
        return !item.done
      })
    }

    // an two example how to filter items on the list
    whatShow(item) {
      return !item.hidden
    }

    onlyDone(item) {
      return item.done
    }

    toggle(e) {
      var item = e.item
      item.done = !item.done
      return true
    }

    
  </script>

</todo>