$(document).ready(function(){

    $('.input_quant').on('input', function(){
        var id_opart= $(this).attr('id_opart');
        $('#cBtn'+id_opart).css('display','block');
        $('#sBtn'+id_opart).css('display','block');
        $('#deleteOpartBtn'+id_opart).css('display','none');
    });

    $('.cancel_btn').on('click', function (){
        var id_opart= $(this).attr('id_opart');
        var val = $('#inp'+id_opart).attr('value');
        $('#inp'+id_opart).prop('value', val);
        $('#cBtn'+id_opart).css('display','none');
        $('#sBtn'+id_opart).css('display','none');
        $('#deleteOpartBtn'+id_opart).css('display','block');
    });

    $('.save_btn').on('click', function(){
        var id_opart= $(this).attr('id_opart');
        var value = $('#inp'+id_opart).prop('value');
        var token =  $('input[name="csrf_token"]').attr('value');
        console.log(value)
        req = $.ajax({
            url : '/retail/'+id_opart+'/update_opart_quant',
            type: 'POST',
            data: {quantity: value},
            headers: {
                'X-CSRF-Token': token
                }
        });
        req.done(function(data){
            $('#showRetailOpart').html(data);
        });  
    });
});
