
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
        }).then(Response => Response.body)
        .then(data => alert(data), data => alert(data))
        .catch(error => console.log(error))
        .finally(window.location.href = 'index.html')
}