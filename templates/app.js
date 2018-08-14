function signup() {
    let creds = $('#creds').serializeArray().reduce(function (obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    fetch('http://127.0.0.1:5000/api/v1/auth/signup', {
            method: 'POST',
            body: JSON.stringify(creds),
            headers: {
                'Content-Type': 'application/json'
            }
        }).catch(error => console.error('Error:', error))
        .then(response => console.log('Success:', response))
}