document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    const createMessage = (message, name, time) => {
        const msg = document.createElement('p');
        const span_username = document.createElement('span');
        const span_message = document.createElement('span');
        const span_timestamp = document.createElement('span');
        var localtime = moment.utc(time).local();
        var calendartime = moment(localtime).calendar();
        const br = document.createElement('br')

        if(name == username) {
            msg.setAttribute("class", "own-msg");
            span_username.setAttribute("class", "own-username");
        } else {
            msg.setAttribute("class", "others-msg");
            span_username.setAttribute("class", "other-username");
        }
        span_username.innerText = name;

        span_timestamp.setAttribute("class", "timestamp");
        span_timestamp.innerText = calendartime;

        span_message.innerText = message;
        msg.innerHTML += span_username.outerHTML +
            br.outerHTML +
            span_message.outerHTML +
            br.outerHTML +
            span_timestamp.outerHTML;

        document.querySelector('#messages').append(msg);
    };

    socket.on('display_message', data => {
        createMessage(data.msg, data.username, data.timestamp);
    });

    document.querySelector('#send_message').onclick = () => {
        socket.emit('user_message', {'msg': document.querySelector('#user_message').value,
            'username': username,
            'user_id': user_id,
            'room_id': room_id});
        document.querySelector('#user_message').value = '';
    };
});
