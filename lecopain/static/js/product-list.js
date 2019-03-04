
function add_fields() {
    var el = document.getElementById('product_id');
    var text = el.options[el.selectedIndex].innerHTML;
    var row_nb = document.getElementById('row_nb');

    document.getElementById('tab_qn_ans').innerHTML += '<tr data-toggle="fieldset-entry" name="tr_'+row_nb.value+'">'
    +'<td><input type="hidden" , name="products" value="'+el.value+'"/>Ref-'+el.value+'</td>'
    +'<td> '+text+' </td>'
    +'<td> <b>x</b> <input type="number" style="width: 7em" name="quantities" value="1"/></td>'
//    +'<td><button type="button" data-toggle="fieldset-remove-row" id="product-'+row_nb.value+'-remove" onclick="remove_fields('+row_nb.value+');">-</button></td> </tr>';
    +'<td><button type="button" id="product-'+row_nb.value+'-remove" onclick="remove_fields('+row_nb.value+');" class="btn btn-warning" ><i class="fa fa-minus"></i></button></td> </tr>';
    document.getElementById("row_nb").value = row_nb.value++
}

function remove_fields(num) {
    document.getElementById("tab_qn_ans").deleteRow(num+1)
}