function hideLoader() {
    $('#loader').hide();
}

function displayMsgPartial() {
    $('#msg-partial').show();
}

function hideMsgPartial() {
    $('#msg-partial').hide();
}

function prepareWindow() {
    hideMsgPartial();
    hideLoader();
}

$(window).ready(prepareWindow);

document.querySelector('#search-submit').onclick = function(e) {
    let twitterCheckboxInputDom = document.querySelector('#twitter-checkbox');
    let twitterCheckbox = twitterCheckboxInputDom.checked;
    let googleSearchCheckboxInputDom = document.querySelector('#google-search');
    let googleSearchCheckbox = googleSearchCheckboxInputDom.checked;
    let dbCheckboxInputDom = document.querySelector('#db-search');
    let dbCheckbox = dbCheckboxInputDom.checked;
    if(!twitterCheckbox && !googleSearchCheckbox && !dbCheckbox) return;

    let form = document.getElementById('card');
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
        'twitter': twitterCheckbox,
        'google': googleSearchCheckbox,
        'db': dbCheckbox
    });

    paramSocket.send(searchData);
};