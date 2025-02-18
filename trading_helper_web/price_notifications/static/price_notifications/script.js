const WS_URL = document.currentScript.getAttribute('data-ws-url');
const CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]').value;

const errorMessage = document.currentScript.getAttribute('data-error-message');
if (errorMessage) {
    alert(errorMessage);
}

const realTimePriceDivs = document.querySelectorAll("[data-track-symbol]");

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

    realTimePriceDivs.forEach((elem) => {
        if (elem.dataset.trackSymbol === tick.symbol) {
            elem.textContent = `${tick.bid}`;
        }
    });
};

connectToWSServer(onWsMessage);

const deleteNotification = async (notificationId) => {
    if (confirm('Are you sure you want to delete this notification?')) {
        await fetch(`/price_notifications/delete_notification/${notificationId}/`, {
            method: 'delete',
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
        });
        location.reload();
    }
};
