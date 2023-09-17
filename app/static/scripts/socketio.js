document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    const createMessage = (name, message) => {
        const timestamp = moment().calendar();
        messages.innerHTML += content;
    };


    socket.on('connect', () => {
        socket.send("I am connected");
    });

    socket.on('message', data => {

        console.log(`Message reeived: ${data}`)
    });
})
