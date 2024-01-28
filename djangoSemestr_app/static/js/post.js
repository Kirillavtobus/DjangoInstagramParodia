$(function(){
    $('#add_comment').click(function(){
        var button = $(this)
        $.ajax(button.data('url'),{
            'type': 'POST',
            'dataType': 'json',
            'async': true,
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'comment': $('#comment').val(),

            },
            'success': function(data){
                document.getElementById('comments').innerHTML += data
            })
        })
    })
}