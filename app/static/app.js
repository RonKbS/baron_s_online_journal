
function signup() {
    form = document.forms[0]
    fetch('http://127.0.0.1:5000/api/v1/auth/signup', {
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify({
                'name': form.name.value,
                'email': form.mail.value,
                'password': form.lock.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(Body => Body.json())
        .then(data => {
            if (data['Message'] === 'Karibu! Let\'s begin by logging in') {
                alert(data['Message']);
                window.location.href = 'index.html';
            }
            else if (data['Message'] != 'Karibu! Let\'s begin by logging in') {
                alert(data['Message']);
                return data['Message'];
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
        .then(reply => {
            if (!reply['Message']) {
                let key = 'token';
                let value = reply['token'];
                localStorage.setItem(key, value);
                console.log(localStorage.getItem('token'));
                window.location.href = 'home_page.html';
            } else if (reply['Message']) {
                return alert(reply['Message'])
            }
            return true;
        })
        .catch(error => alert(error))
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
}

function add_entry() {
    if (!localStorage.getItem('title')) {
        fetch('http://127.0.0.1:5000/api/v1/entries', {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            cache: 'reload',
            body: JSON.stringify({
                'title': document.getElementById('title').value,
                'content': document.getElementById('content').value
            }),
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            if (data['Message'] === 'Entry added') {
                alert('Thoughts immortalized!!');
                return window.location.href = 'home_page.html';
            }
            else if (data['Message'] != 'Entry added') {
                alert(data['Message']);
                return data['Message'];
            }
        })
        .catch(error => console.error(error))
    }
    else {
        update_entry();
    }

}

function display_entries() {
    let t = document.getElementById('entries_table');
    fetch('http://127.0.0.1:5000/api/v1/entries', {
            method: 'GET',
            credentials: 'include',
            cache: 'reload',
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            if (data['Entries'] != 'No entries') {
                let list_entries = data['Entries'];
                let len = list_entries.length;
                for (let x = 0; x < len; x++) {
                    let r = document.createElement('tr');
                    t.insertBefore(r, t.childNodes[0])
                    let c = r.insertCell();
                    c.className = 'each';
                    let box = document.createElement("input");
                    box.setAttribute('type', 'checkbox')
                    c.appendChild(box)
                    let title = document.createElement("input");
                    title.className = 'appear';
                    title.setAttribute("id", x);
                    title.setAttribute("type", 'button');
                    title.setAttribute("onclick", "get_entry()");
                    title.setAttribute("value", list_entries[x]['title']);
                    c.appendChild(title);
                    
                }
                return true;
            }
            else if (data['Entries'] === 'No entries') {
                let r = t.insertRow();
                    let c = r.insertCell();
                    let title = document.createElement("input");
                    title.className = 'each';
                    title.setAttribute("type", 'button');
                    title.setAttribute("onclick", 'get_entry()');
                    title.setAttribute("value", data['Entries']);
                    c.appendChild(title);
            }
        })
        .catch(error => console.error(error))
}

function get_entry() {
    let entry = event.currentTarget;
    if (!entry.getAttribute('id')) {
        return window.location.href = 'entry.html';
    }
    let t = entry.getAttribute('value');
    fetch('http://127.0.0.1:5000/api/v1/entries', {
            method: 'GET',
            mode: 'cors',
            credentials: 'include',
            cache: 'reload',
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            let listEntries = data['Entries'];
            let len = listEntries.length;
            for (let x = 0; x < len; x++) {
                if (listEntries[x]['title'] === t) {
                    localStorage.setItem('title', listEntries[x]['title'])
                    localStorage.setItem('content', listEntries[x]['content'])
                    return window.location.href = 'entry.html'
                }
            }
        })
        .catch(error => console.error(error))

}

function view_entry() {
    if (localStorage.getItem('title')) {    
        let t = document.getElementById('title')
        t.value = localStorage.getItem('title');
        let c = document.getElementById('content');
        c.value = localStorage.getItem('content');
        localStorage.removeItem('content');
        return true;
    }
    return false;
}

async function return_id() {
    await fetch('http://127.0.0.1:5000/api/v1/entries', {
            method: 'GET',
            credentials: 'include',
            cache: 'reload',
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            let id;
            let t = localStorage.getItem('title');
            localStorage.removeItem('title');
            let listEntries = data['Entries'];
            let len = listEntries.length;
            for (let x = 0; x < len; x++) {
                if (listEntries[x]['title'] === t) {
                    id = listEntries[x]['entry_id']
                    localStorage.setItem('id', id)
                }
            }
            return id
        })
}

async function update_entry() {
    await return_id();
    let id = localStorage.getItem('id')
    localStorage.removeItem('id')
    fetch('http://127.0.0.1:5000/api/v1/entries/' + id, {
        method: 'PUT',
        mode: 'cors',
        credentials: 'include',
        cache: 'reload',
        body: JSON.stringify({
            'title': document.getElementById('title').value,
            'content': document.getElementById('content').value
        }),
        headers: {
            'Content-Type': 'application/json',
            'token': localStorage.getItem('token')
        }
    }).then(Body => Body.json())
    .then(data => {
        if (data['Message'] === 'Entry has been modified') {
            alert('Thoughts updated!!');
            localStorage.removeItem('id')
            return window.location.href = 'home_page.html';
        }
        else if (data['Message'] != 'Entry has been modified') {
            alert('No changes made');
            return window.location.href = 'home_page.html';
        }
    })
    .catch(error => console.error(error))
}

async function delete_entry() {
    await return_id();
    let id = localStorage.getItem('id')
    localStorage.removeItem('id')
    fetch('http://127.0.0.1:5000/api/v1/entries/' + id, {
        method: 'DELETE',
        mode: 'cors',
        credentials: 'include',
        cache: 'reload',
        headers: {
            'Content-Type': 'application/json',
            'token': localStorage.getItem('token')
        }
    }).then(Body => Body.json())
    .then(data => {
    if (data['Message'] === 'Entry deleted') {
        alert('Thoughts removed!!');
        localStorage.removeItem('id')
        return window.location.href = 'home_page.html';
    }
    else if (data['Message'] != 'Entry deleted') {
        alert('No changes made');
        return window.location.href = 'home_page.html';
        }
    })
    .catch(error => console.error(error))
}

function delete_several() {
    let checked_box = document.querySelectorAll('input')
    checked_box.forEach(async function(box){
        if (box.getAttribute('type') === 'checkbox' & box.checked) {
            let title = box.nextSibling.value
            localStorage.setItem('title', title)
            await return_id();
            await delete_entry();
        }
    })
}


function same_password() {
    form = document.forms[0]
    if (form.new_p1.value == form.new_p2.value) {
        document.getElementById('message').innerHTML = 'matching';
    }
    else {
        document.getElementById('message').innerHTML = 'not matching';
    }
}


function update_details() {
    form1 = document.forms[0]
    form2 = document.forms[1]
    if (form1.new_p2.value) {
        let details = form1.new_p2.value;
        fetch('http://127.0.0.1:5000/api/v1/account', {
            method: 'PUT',
            mode: 'cors',
            credentials: 'include',
            cache: 'reload',
            body: JSON.stringify({
                'password': details
            }),
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            if (data['Message'] === 'Password has been changed') {
                alert(data['Message']);
            }
            else if (data['Message'] != 'Password has been changed') {
                alert('No changes made');
        }
    })
        .catch(error => console.error(error))
    }
    else {
        let details = form2.email.value;
        fetch('http://127.0.0.1:5000/api/v1/account', {
            method: 'PUT',
            mode: 'cors',
            credentials: 'include',
            cache: 'reload',
            body: JSON.stringify({
                'email': details
            }),
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            if (data['Message'] === 'Email has been changed') {
                alert(data['Message']);
            }
            else if (data['Message'] != 'Email has been changed') {
                alert('No changes made');
        }
    })
        .catch(error => console.error(error))
    }
}
