function display_loading() {
    let link = document.getElementById('content');
    link.style.display = 'none';
    link = document.getElementById('wait');
    link.style.display = 'block';
}