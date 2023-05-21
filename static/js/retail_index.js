$(document).ready(function(){

    $('.retailOp').on('click', function(){
        var id_op = $(this).attr('id_op');
        console.log(id_op)
        req=$.ajax({
            type: "GET",
            url:  "/retail/"+id_op+"/retail_opart",
        });
        req.done(function(data){
            $('#retailOpart').html(data);
        });     
    });

});
