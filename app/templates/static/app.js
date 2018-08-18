
function signup() {
    fetch('http://127.0.0.1:5000/api/v1/auth/signup', {
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify({
                'name': document.getElementById('name').value,
                'email': document.getElementById('mail').value,
                'password': document.getElementById('lock').value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(Body => Body.json())
        .then(data => alert(data['Message']))
        // .then(window.location.href = 'index.html')
}
function login() {
    fetch('http://127.0.0.1:5000/api/v1/login', {
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify({
                'name': document.getElementById('name').value,
                'password': document.getElementById('lock').value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(Body => Body.json())
        .catch(error => alert(error))
        .then(reply => alert(reply['Message']))
        // Return window.alert(reply())
        /* .then(window.location.href = 'index.html')*/
}