$(document).ready(function(){
    $('.chekOpart').on('change', function(){
        if ($("input:checked").length == 1){
            if ($(this).prop('checked')){
                $('#btnOpartChange').removeClass('disabled')
                $('#btnOpartDelete').removeClass('disabled')

                // $('#btnOpartChange').prop('disabled', false);
                // $('#btnOpartDelete').prop('disabled', false);
            }
            
            else{
                if ($(this).prop('checked') != true){
                    $('#btnOpartChange').removeClass('disabled')
                    $('#btnOpartDelete').removeClass('disabled')

                    // $('#btnOpartChange').prop('disabled', false);
                    // $('#btnOpartDelete').prop('disabled', false);
                }
                else {
                    $('#btnOpartChange').addClass('disabled')
                    $('#btnOpartDelete').addClass('disabled')

                    // $('#btnOpartChange').prop('disabled', true);
                    // $('#btnOpartDelete').prop('disabled', true);
                }
            };
        }
        else {
            $('#btnOpartChange').addClass('disabled')
            $('#btnOpartDelete').addClass('disabled')

            // $('#btnOpartChange').prop('disabled', true);
            // $('#btnOpartDelete').prop('disabled', true);
        };
        

    });
    $('#btnOpartChange').on('click', function(){
        var id_opart = $('input:checked').attr('id_opart')
        $(this).prop('href', '/wms/opart/'+id_opart+'/update_opart')
    });

    $('#btnOpartDelete').on('click', function(){
        var id_opart = $('input:checked').attr('id_opart')
        // delete_opart
        $(this).prop('href', '/wms/opart/'+id_opart+'/delete_opart')

    });
});
