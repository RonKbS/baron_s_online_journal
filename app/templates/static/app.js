// https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js

$(document).ready(function (){
    function signup() {
        //let form = document.getElementById('creds');
        fetch('http://localhost/api/v1/auth/signup', {
                method: 'POST',
                mode: 'cors',
                body: JSON.stringify({
                    'name': document.getElementById('name'),
                    'email': document.getElementById('mail'),
                    'password': document.getElementById('lock')
                })
            })
            .then(response => console.log('Success:', response.json()))
            .catch(error => console.error('Error:', error))
    }
});