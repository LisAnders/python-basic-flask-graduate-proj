$(document).ready(function(){
    $('.artDetail').on('dblclick', function(){
        var id_art = $(this).attr('id_art');
        window.location.href = '/wms/article/' + id_art;     
    });
    
    $('.chekArticle').on('change', function(){
        if ($("input:checked").length == 1){
            if ($(this).prop('checked')){
                $('#btnRestInfo').removeClass('disabled');
            }
            
            else{
                if ($(this).prop('checked') != true){
                    $('#btnRestInfo').removeClass('disabled');
                }
                else {
                    $('#btnRestInfo').addClass('disabled');
                }
            };
        }
        else {
            $('#btnRestInfo').addClass('disabled');
        };
    });

    $('#btnRestInfo').on('click', function(){
        var id_art = $('input:checked').attr('id_art')
        $(this).prop('href', '/wms/article/'+id_art+'/show_article_rest')
    });

});
