let paramSocket = new WebSocket('ws://' + window.location.host);

paramSocket.onmessage = function(e) {
    hideLoader();
    displayMsgPartial();
    console.log("Some result are ready");
    setTimeout(function () {
        window.location.href = "http://127.0.0.1:8000/graph";
    }, 3000);
};
