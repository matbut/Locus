let chatSocket = new WebSocket('ws://' + window.location.host + '/ws/search/');

console.log("hello");

chatSocket.onmessage = function(e) {
    window.location.href = "http://127.0.0.1:8000/tables";
};

document.querySelector('#search-submit').onclick = function(e) {
    let form = document.querySelector('#content-wrapper > center > div.card.card-login.mx-auto.mt-5')
    form.style.display = 'none';
    let loader = document.getElementById('loader');
    loader.style.display = 'block';
    let loader_img = document.getElementById('loader-img');
    loader.style.display = 'block';

    let messageInputDom = document.querySelector('#url');
    let message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'url': message
    }));

    console.log(message);

    messageInputDom.value = '';
};
