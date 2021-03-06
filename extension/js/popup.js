var dot = document.getElementById('dot')
var status = document.getElementById('status')
var connection = document.getElementById('connection')

if (globalThis.ws.readyState === 1) { // Connected
    dot.classList.add('colors-online')
    status.innerHTML = 'Connected'
    connection.innerHTML = 'Disconnect'
} else if (globalThis.ws.readyState === 0) { // Connecting
    dot.classList.add('colors-connecting')
    status.innerHTML = 'Connecting...'
    connection.setAttribute(disabled, true)
} else if (globalThis.ws.readyState === 3) { // Disconnected
    dot.classList.add('colors-offline')
    status.innerHTML = 'Failed to connect'
    connection.innerHTML = 'Connect'
}