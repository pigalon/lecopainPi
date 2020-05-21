
<todo>

  <h3>{ opts.title }</h3>

  <!--<ul>
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
  </form>-->


  <table>
  <tr>
  <td>
  <select class="form-control" ref="seller" width="300px" onchange={ load_products }>
    <option each="{ seller in sellers }" value={seller.id}> {seller.name} </option> 
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

   <form onsubmit={ products }>
    <button type="button" disabled={ products.filter(onlyDone).length == 0 } onclick={ removeAllDone }>
    X{ items.filter(onlyDone).length } </button>
  </form>

  <ul>
    <li each={ selected_products.filter(whatShow) }>
      <label class={ completed: done }>
        <input type="hidden" name="products" value="{id}"/> 
        <input type="checkbox" checked={ done } onclick={ parent.toggle }> { id } - { name }</input>
      </label>
    </li>
  </ul>


  <!-- this script tag is optional -->
  <script>

    var self = this

    this.items = opts.items
    this.selected_products = opts.selected_products

    this.sellers = []
    this.products = []

    /******************************************
     at page init : 
       mount riotjs module
       load sellers list
    *******************************************/
    
    this.on('mount', function(){
      self.load_sellers()
    })

    /******************************************
       load sellers list
    *******************************************/

    load_sellers(){
      var url = 'http://localhost:5000/apisellers/'; //random adress
      $.ajax({
            url: url,
            type: "GET",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(data) {
              self.sellers = data['sellers']
              self.update()
            }
        });
    }

    /******************************************
       load products list
    *******************************************/
    load_products(){
        seller_id = this.refs.seller.value
        var url = 'http://localhost:5000/apiproducts/'+seller_id;
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

    /******************************************
       add product to the list (baket)
    *******************************************/
    addProduct(e){
      
      product_id = this.refs.product.value
      product_name = this.refs.product[product_id].text
      

      console.log('product_id : ' + product_id + ' - ' + product_name)

      if (product_name) {
        this.selected_products.push({ id : product_id, name: product_name })
        //this.text = this.refs.input.value = ''
      }
      e.preventDefault()

    }

    /*allTodos(){
      
      var test = [{done:'true', due_date:'11', title:'the title'}, {done:'true', due_date:'11', title:'the title'}]
      return test
    }*/

   /* await mount_sellers(){

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
      this.products = this.products.filter(function(product) {
        return !product.done
      })
    }

    // an two example how to filter items on the list
    whatShow(product) {
      return !product.hidden
    }

    onlyDone(product) {
      return product.done
    }

    toggle(e) {
      var product = e.product
      product.done = !product.done
      return true
    }

    
  </script>

</todo>