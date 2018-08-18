
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
        .then(data => {
            alert(data['Message'])
            return data['Message']
        })
        .finally(message => {
            if (message === 'User added') {
                window.location.href = 'index.html'
            }
        })
}
function login() {
    fetch('http://127.0.0.1:5000/api/v1/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'name': document.getElementById('name').value,
                'password': document.getElementById('lock').value
            }),
            mode: 'cors',
            redirect: 'manual'
        })
        .then(Response => Response.json())
        .then(reply => console.log(reply['Message']))
        .catch(error => alert(error))
        // Return window.alert(reply())
        /* .then(window.location.href = 'index.html')*/
}