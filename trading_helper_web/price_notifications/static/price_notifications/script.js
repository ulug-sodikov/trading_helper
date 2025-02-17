const WS_URL = document.currentScript.getAttribute('data-ws-url');

const error_message = document.currentScript.getAttribute('data-error-message');
if (error_message) {
    alert(error_message);
}

const connectToWSServer = (onMessage) => {
    const socket = new WebSocket(WS_URL);
    // If connection is failed reestablish connection after 2 seconds.
    socket.addEventListener("close", () => {
        setTimeout(connectToWSServer, 2000, onMessage);
    });
    socket.addEventListener("message", onMessage);
};

const onWsMessage = (event) => {
    const tick = JSON.parse(event.data);
    if (tick.symbol === 'XAUUSD') {
        // This spread calculation is only valid for XAUUSD
        const xauusdSpread = tick.ask*100 - tick.bid*100;
        const priceDiv = document.getElementById('instrument-price-number');
        const spreadDiv = document.getElementById('instrument-spread-info');
        priceDiv.textContent = `${tick.bid}`;
        spreadDiv.textContent = `SPREAD ${xauusdSpread} PIPS`;
    }
};

connectToWSServer(onWsMessage);
