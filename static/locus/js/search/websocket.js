let paramSocket = new WebSocket('ws://' + window.location.host + '/ws/search/');

paramSocket.onmessage = function(e) {
    window.location.href = "http://127.0.0.1:8000/tables";
};

document.querySelector('#search-submit').onclick = function(e) {
    let twitterCheckboxInputDom = document.querySelector('#twitter-checkbox');
    let twitterCheckbox = twitterCheckboxInputDom.checked;
    if(!twitterCheckbox) return;

    let form = document.querySelector('#content-wrapper > center > div.card.card-login.mx-auto.mt-5');
    form.style.display = 'none';
    let loader = document.getElementById('loader');
    loader.style.display = 'block';

    let urlInputDom = document.querySelector('#url');
    let url = urlInputDom.value;
    let titleInputDom = document.querySelector('#title');
    let title = titleInputDom.value;
    let contentInputDom = document.querySelector('#art-content');
    let content = contentInputDom.value;

    let searchData = JSON.stringify({
        'url': url,
        'title': title,
        'content': content,
        'twitter': twitterCheckbox
    });

    paramSocket.send(searchData);
};
