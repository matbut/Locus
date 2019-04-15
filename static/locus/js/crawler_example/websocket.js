let chatSocket = new WebSocket('ws://' + window.location.host + '/ws/search/');
var responses = 0;

console.log("hello");

chatSocket.onmessage = function(e) {
    responses += 1;
    console.log(responses);
    if(responses === 3) {
        window.location.href = "http://127.0.0.1:8000/result";
    }
};

document.querySelector('#search-submit').onclick = function(e) {
    let link = document.getElementById('content');
    link.style.display = 'none';
    link = document.getElementById('wait');
    link.style.display = 'block';

    var messageInputDom = document.querySelector('#search-input');
    var message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));

    messageInputDom.value = '';
};