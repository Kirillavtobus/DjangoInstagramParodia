
$(function(){
    $('#btn_post_create').click(function(){
        var button = $(this)
        $.ajax(button.data('url'),{
            'type': 'POST',
            'dataType': 'json',
            'async': true,
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),

            }
        })})
})