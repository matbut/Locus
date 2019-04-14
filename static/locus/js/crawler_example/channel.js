$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/sw" + window.location.pathname);

    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        // redirect to result
    };
});
