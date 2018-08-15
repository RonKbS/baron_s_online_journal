//https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js

let form = document.getElementById('creds');

function signup() {
    GlobalFetch.fetch('http://localhost/api/v1/auth/signup', {
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