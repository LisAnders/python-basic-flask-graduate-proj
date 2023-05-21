$(document).ready(function(){

    $('.typeOp').on('click', function(){

        var id_top = $(this).attr('id_top');
        var token =  $('input[name="csrf_token"]').attr('value');

        // console.log(id_top);
        req = $.ajax({
            url : '/operation/warehouse',
            type: 'POST',
            data: {id_top: id_top},
            headers: {
                'X-CSRF-Token': token 
           },
        })
        req.done(function(data){
            $('#warehouseID').html(data);
        });  
    });

    $('.saveBtn').on('click',function(){
        var id_top = $('option[class="typeOp"]').arrt('id_top');
        var token =  $('input[name="csrf_token"]').attr('value');
        console.log(id_top);
        req = $.ajax({
            url : '/operation/create',
            type: 'POST',
            data: {id_top: 'TOP'},
            headers: {
                'X-CSRF-Token': token 
           },
        })
    });

});