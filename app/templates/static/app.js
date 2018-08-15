
function signup() {
    // Let form = document.getElementById('creds');
    fetch('http://127.0.0.1:5000/api/v1/auth/signup', {
            method: 'POST',
            body: JSON.stringify({
                'name': document.getElementById('name').value,
                'email': document.getElementById('mail').value,
                'password': document.getElementById('lock').value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => console.log('Success:', response.json()))
        .catch(error => console.error('Error:', error))
}