

function getSettings() {
    // Теперь значения будут отправлены на сервер Flask для обработки
    const idInstance = document.getElementById("idInstance").value;
    const apiTokenInstance = document.getElementById("apiTokenInstance").value;

    fetch(`/get_settings?idInstance=${idInstance}&apiTokenInstance=${apiTokenInstance}`, {
        method: 'GET'
    })
    // Остальная часть функции остаётся прежней
}

function getSettings() {
    // Теперь значения будут отправлены на сервер Flask для обработки
    const idInstance = document.getElementById("idInstance").value;
    const apiTokenInstance = document.getElementById("apiTokenInstance").value;

    fetch(`/get_settings?idInstance=${idInstance}&apiTokenInstance=${apiTokenInstance}`, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        document.getElementById("response").value = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}

function getStateInstance() {
    const idInstance = document.getElementById("idInstance").value;
    const apiTokenInstance = document.getElementById("apiTokenInstance").value;

    fetch(`/state_instance?idInstance=${idInstance}&apiTokenInstance=${apiTokenInstance}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("response").value = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error('Error:', error));
}


function sendMessage() {
    const idInstance = document.getElementById("idInstance").value;
    const apiTokenInstance = document.getElementById("apiTokenInstance").value;
    const phoneNumber = document.getElementById("phoneNumber").value;
    const messageText = document.getElementById("messageText").value;

    // Убедитесь, что поля не пустые
    if (!idInstance || !apiTokenInstance || !phoneNumber || !messageText) {
        console.error("All fields must be filled");
        return;
    }

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            idInstance: idInstance, // добавлено поле для idInstance
            apiToken: apiTokenInstance, // добавлено поле для apiTokenInstance
            phone: phoneNumber + '@c.us',
            message: messageText
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("response").value = JSON.stringify(data, null, 2);
        // Очистка полей после отправки
        document.getElementById("phoneNumber").value = '';
        document.getElementById("messageText").value = '';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}



function sendFileByUrl() {
    const idInstance = document.getElementById("idInstance").value;
    const apiTokenInstance = document.getElementById("apiTokenInstance").value;
    const phoneNumber = document.getElementById("phoneNumber").value;
    const fileUrl = document.getElementById("fileUrl").value;

    fetch('/send_file_by_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            idInstance: idInstance,
            apiTokenInstance: apiTokenInstance,
            phone: phoneNumber + '@c.us',
            fileUrl: fileUrl
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").value = JSON.stringify(data, null, 2);
        // Очистка поля URL после отправки
        document.getElementById("fileUrl").value = '';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




console.log("Script file is loaded and running");
