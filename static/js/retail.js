$(document).ready(function(){
    // console.log($('#showRetailOpart').attr('id_op'))
    var id_op = $('#showRetailOpart').attr('id_op')
    $('#showRetailOpart').load('/retail/'+id_op+'/show_opart');
    // $('.confirm_sold').on('click', function () {
    //     req =$.ajax({
    //         url: '/retail/'+id_op+'/confirm_sold',
    //         type: 'GET',
    //     })
    // });
});
