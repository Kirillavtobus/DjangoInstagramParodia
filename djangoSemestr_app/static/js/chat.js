function sendMessage(){
    $('#input').click(function(){
    var btn = $(this);
    console.log(btn);
    console.log(data['message']);
    $.ajax(btn.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'message': document.getElementById('id_body').value,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'success': function(data){
            document.getElementById('messages').innerHTML += '<p class="u_msg">' + data['message'] + '</p><br>';
            document.getElementById('id_body').value = '';
        }
    })
    })
}

$(document).ready(function(){
    sendMessage();
})