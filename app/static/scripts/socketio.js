const socket = io();
let message_list = document.getElementById('user_messages_list');
message_list.scrollIntoView(false);
let client_window = document.getElementById('messages_div');
joinRoom(room_id);

const createMessage = (message, name, time, avatar_url, id) => {
    const list_item = document.createElement('li');
    const msg = document.createElement('div');
    const msgHeader = document.createElement('div');
    const strong = document.createElement('strong');
    const span_username = document.createElement('a');
    const align_span = document.createElement('span');
    const delete_button = document.createElement('button');
    const x_span = document.createElement('span');
    const span_message = document.createElement('span');
    const span_timestamp = document.createElement('span');
    const img_avatar = document.createElement('img');
    var localtime = moment.utc(time).local();
    var calendartime = moment(localtime).calendar();

    if (name == username) {
        msg.setAttribute('class', 'p-2 w-100');
        div_id = 'message_id_' + id;
        msg.setAttribute('id', div_id);
        span_username.setAttribute('href', '/user/' + name);
        list_item.setAttribute(
            'class',
            'own_message list-group-item d-flex justify-content-between align-items-start p-2 w-100'
        );
    } else {
        msg.setAttribute('class', 'p-2 w-100');
        list_item.setAttribute(
            'class',
            'other_message list-group-item d-flex justify-content-between align-items-start p-2 w-100'
        );
    }

    msgHeader.setAttribute(
        'class',
        'header fw-bold d-flex justify-content-between p-2 w-100'
    );

    img_avatar.setAttribute('src', avatar_url);

    strong.innerText = name;
    span_username.innerHTML += strong.outerHTML;

    align_span.setAttribute('class', 'align-items-center');

    span_timestamp.innerText = calendartime;
    align_span.innerHTML += span_timestamp.outerHTML;

    // Delete button creation
    delete_button.setAttribute('type', 'button');
    delete_button.setAttribute('class', 'close');
    const param = 'deleteMessage(' + id + ')';
    delete_button.setAttribute('onclick', param);
    x_span.setAttribute('aria-hidden', 'true');
    x_span.innerHTML = '&times;';
    delete_button.innerHTML += x_span.outerHTML;

    if (name == username) {
        align_span.innerHTML += delete_button.outerHTML;
    }

    msgHeader.innerHTML +=
        img_avatar.outerHTML + span_username.outerHTML + align_span.outerHTML;

    span_message.innerText = message;

    msg.innerHTML += msgHeader.outerHTML + span_message.outerHTML;

    list_item.innerHTML += msg.outerHTML;

    // document.querySelector('#user_messages_list').append(list_item);
    message_list.append(list_item);
};

socket.on('user_message', (data) => {
    createMessage(
        data.msg,
        data.username,
        data.timestamp,
        data.avatar_url,
        data.id
    );
    if (
        client_window.scrollTop + client_window.clientHeight * 1.5 >=
        message_list.scrollHeight
    ) {
        message_list.scrollIntoView(false);
    }
});

socket.on('connect_error', (err) => {
    console.log(`connect_error due to ${err.message}`);
});

document.querySelector('#send_message').onclick = () => {
    socket.emit('user_message', {
        msg: document.querySelector('#user_message').value,
        username: username,
        user_id: user_id,
        room_id: room_id,
        avatar_url: avatar_url,
    });
    document.querySelector('#user_message').value = '';
};

function joinRoom(room_id) {
    socket.emit('join', { room_id: room_id });
    document.querySelector('#user_message').innerHTML = '';
    document.querySelector('#user_message').focus();
}

socket.on('delete_message', (data) => {
    console.log('recieved delete_message');
    div_id = '#message_id_' + data.message_id;
    console.log(div_id);
    document.querySelector(div_id).parentNode.remove();
});

function deleteMessage(message_id) {
    socket.emit('delete_message', {
        room_id: room_id,
        message_id: message_id,
        user_id: user_id,
    });
}
