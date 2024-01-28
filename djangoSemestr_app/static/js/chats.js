$(function(){
    $(document).click(function(event) {
    b_id = $(event.target);
    console.log(b_id);
    if (b_id.attr('class') == 'profile-image pr-3' || b_id.attr('class') == null || b_id.attr('class') == 'btn_snd open mx-2'){
        if (document.getElementById('chat').innerHTML == '') {
            $.ajax(b_id.data('url'), {
                'type': 'POST',
                'async': true,
                'dataType': 'json',
                'data': {
                    'chat': b_id.data('id'),
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                'success': function(data){
                    document.getElementById('chat').innerHTML += data;
                }
            })
        } else {
            document.getElementById('chat').innerHTML = '';
        }


    }else if (b_id.attr('id') == 'input'){
        $.ajax(b_id.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'message': document.getElementById('id_body').value,
                'chat': b_id.data('id'),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'success': function(data){
                document.getElementById('messages').innerHTML += '<div class="row"><div> <p class="u_msg float-end">' + data['message'] + '</p><br></div></div>';
                document.getElementById('id_body').value = '';
            }
        })
    }
    })})