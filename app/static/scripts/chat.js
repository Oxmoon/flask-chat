document.addEventListener('DOMContentLoaded', () => {
    let button = document.getElementById("send_message");
    let textBox = document.getElementById("user_message");
    textBox.addEventListener("keyup", function (event) {
        if (event.key === 'Enter') {
            button.click();
        }
    });
});
