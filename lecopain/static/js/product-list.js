$(function() {
    $("div[data-toggle=fieldset]").each(function() {
        var $this = $(this);
            
        //Add new entry
        $this.find("button[data-toggle=fieldset-add-row]").click(function() {
            var target = $($(this).data("target"));
            console.log(target);
            var oldrow = target.find("[data-toggle=fieldset-entry]:last");
            var row = oldrow.clone(true, true);
            console.log(row.find(":select")[0]);
            var elem_id = row.find(":select")[0].id;
            var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
            row.attr('data-id', elem_num);
            row.find(":select").each(function() {
                console.log(this);
                var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
                $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
            });
            row.show();
            oldrow.after(row);
        }); //End add new entry

        //Remove row
        $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
            if($this.find("[data-toggle=fieldset-entry]").length > 1) {
                var thisRow = $(this).closest("[data-toggle=fieldset-entry]");
                thisRow.remove();
            }
        }); //End remove row
    });
});

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