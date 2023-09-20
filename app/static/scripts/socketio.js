document.addEventListener('DOMContentLoaded', () => {
    var socket = io();
    let message_list = document.getElementById('user_messages_list');
    message_list.scrollIntoView(false);
    let client_window = document.getElementById('messages_div')

    const createMessage = (message, name, time, avatar_url) => {
        const list_item = document.createElement('li');
        const msg = document.createElement('div');
        const msgHeader = document.createElement('div');
        const strong = document.createElement('strong');
        const span_username = document.createElement('a');
        const span_message = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const img_avatar = document.createElement('img');
        var localtime = moment.utc(time).local();
        var calendartime = moment(localtime).calendar();

        if(name == username) {
            msg.setAttribute("class", "p-2 w-100");
            span_username.setAttribute("href", ('/user/' + name));
            list_item.setAttribute("class", "own_message list-group-item d-flex justify-content-between align-items-start p-2 w-100");
        } else {
            msg.setAttribute("class", "p-2 w-100 list-group-item d-flex justify-content-between align-items-start p-2 w-100");
            list_item.setAttribute("class", "other_message");
        }
        
        msgHeader.setAttribute("class", "fw-bold d-flex justify-content-between p-2 w-100");

        img_avatar.setAttribute("src", avatar_url);
        img_avatar.setAttribute("class", "avatar");

        strong.innerText = name;
        span_username.innerHTML += strong.outerHTML;

        span_timestamp.setAttribute("class", "timestamp");
        span_timestamp.innerText = calendartime;

        msgHeader.innerHTML += img_avatar.outerHTML +
            span_username.outerHTML + span_timestamp.outerHTML;

        span_message.innerText = message;

        msg.innerHTML += msgHeader.outerHTML +
            span_message.outerHTML;

        list_item.innerHTML += msg.outerHTML;

        // document.querySelector('#user_messages_list').append(list_item);
        message_list.append(list_item);
    };

    socket.on('display_message', data => {
        createMessage(data.msg, data.username, data.timestamp, avatar_url);
            console.log(client_window.scrollTop, client_window.clientHeight, message_list.scrollHeight);
        if (client_window.scrollTop + (client_window.clientHeight * 1.5) >= message_list.scrollHeight) {
            message_list.scrollIntoView(false);
        }
    });

    document.querySelector('#send_message').onclick = () => {
        socket.emit('user_message', {
            'msg': document.querySelector('#user_message').value,
            'username': username,
            'user_id': user_id,
            'room_id': room_id});
        document.querySelector('#user_message').value = '';
    };

});
