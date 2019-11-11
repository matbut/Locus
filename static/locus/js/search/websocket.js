let paramSocket = new WebSocket('ws://' + window.location.host);

paramSocket.onmessage = function(e) {
    window.location.href = "http://127.0.0.1:8000/charts";
};
