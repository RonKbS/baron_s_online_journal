form = new FormData(document.getElementById('creds'))

function signup() {
    fetch('http://127.0.0.1:5000/api/v1/auth/signup', {
            method: 'POST',
            body: JSON.stringify({
                'name': form.get('name'),
                'email': form.get('mail'),
                'password': form.get('lock')
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).catch(error => console.error('Error:', error))
        .then(response => console.log('Success:', response.json()))
}