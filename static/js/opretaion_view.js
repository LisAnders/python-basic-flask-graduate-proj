$(document).ready(function(){
    $('.opArt').on('click', function(){
        var id_op = $(this).attr('id_op');
        console.log(id_op)
        req=$.ajax({
            type: "GET",
            url:  "/wms/opart/"+id_op,
        });
        req.done(function(data){
            $('#showOpart').html(data);
        });     
    });
    $('#createOp').load('/wms/operation/create');
    
});
