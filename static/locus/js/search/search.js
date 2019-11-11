function hideLoader() {
    $('#loader').hide();
}

$(window).ready(hideLoader);

document.querySelector('#search-submit').onclick = function(e) {
    let twitterCheckboxInputDom = document.querySelector('#twitter-checkbox');
    let twitterCheckbox = twitterCheckboxInputDom.checked;
    let googleSearchCheckboxInputDom = document.querySelector('#google-search');
    let googleSearchCheckbox = googleSearchCheckboxInputDom.checked;
    if(!twitterCheckbox && !googleSearchCheckbox) return;

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
        'google': googleSearchCheckbox
    });

    paramSocket.send(searchData);
};