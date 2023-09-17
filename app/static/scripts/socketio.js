document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    const createMessage = (name, message) => {
        const timestamp = moment().calendar();
        const message = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br')

        if(name == username) {
            p.setAttribute("class", "own-msg");
            span_username.setAttribute("class", "own-username");
        } else {
            p.setAttribute("class", "others-msg");
            span_username.setAttribute("class", "other-username");
        }
        span_username.innerText = name;

        span_timestamp.setAttribute("class", "timestamp");
        span_timestamp.innerText = timestamp;

        message.innerHTML += span_username.outerHTML +
            br.outerHTML +
            data.message +
            br.outerHTML +
            span_timestamp.outerHTML;

        document.querySelector('#messages').append(message);
    };


    socket.on('connect', () => {
        socket.send("I am connected");
    });

    socket.on('message', data => {
        createMessage(data.username, data.message);
    });

    document.querySelector('#send_message').onclick = () => {
        socket.send({'message': document.querySelector('#user_message').value,
        'username': username });
        createMessage(document.querySelector('#user_message').value, username);
    };
});
