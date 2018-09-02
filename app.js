
// const url = 'http://127.0.0.1:5000/'
const url = 'https://baron-s-mydiary.herokuapp.com/'

function signup() {
    form = document.forms[0]
    fetch(url + 'api/v1/auth/signup', {
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
    fetch(url + 'api/v1/login', {
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
    let button = event.currentTarget;
    if (!localStorage.getItem('title')) {
        fetch(url + 'api/v1/entries', {
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
            if (data['Message'] != 'Token is invalid!'
                 && data['Message'] === 'Entry added') {
                // let modal = document.getElementById('modal_div')
                // modal.style.display = 'block'
                alert('Entry saved!!')
                return window.location.href = 'home_page.html';
            }
            else if (data['Message'] === 'Token is invalid!') {
                alert('Please login first');
                window.location.href = 'index.html';
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
    fetch(url + 'api/v1/entries', {
            method: 'GET',
            credentials: 'include',
            cache: 'reload',
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            if (data['Message'] != 'Token is invalid!' 
                && data['Message'] != 'No entries') {
                let list_entries = data['Message'];
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
            else if (data['Message'] != 'Token is invalid!' 
                    && data['Message'] === 'No entries') {
                let r = t.insertRow();
                    let c = r.insertCell();
                    c.className = 'each';
                    let title = document.createElement("input");
                    title.className = 'appear';
                    title.setAttribute("type", 'button');
                    title.setAttribute("onclick", 'get_entry()');
                    title.setAttribute("value", data['Message']);
                    c.appendChild(title);
            }
            else if (data['Message'] === 'Token is invalid!') {
                alert('Please login first');
                window.location.href = 'index.html';
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
    fetch(url + 'api/v1/entries', {
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
            if (data['Message'] != 'Token is invalid!') {
                let listEntries = data['Message'];
                let len = listEntries.length;
                for (let x = 0; x < len; x++) {
                    if (listEntries[x]['title'] === t) {
                        localStorage.setItem('title', listEntries[x]['title'])
                        localStorage.setItem('content', listEntries[x]['content'])
                        return window.location.href = 'entry.html'
                    }
                }
            }
            else if (data['Message'] === 'Token is invalid!') {
                alert('Please login first');
                window.location.href = 'index.html';
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
    await fetch(url + 'api/v1/entries', {
            method: 'GET',
            credentials: 'include',
            cache: 'reload',
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            if (data['Message'] != 'Token is invalid!') {
                let id;
                let t = localStorage.getItem('title');
                localStorage.removeItem('title');
                let listEntries = data['Message'];
                let len = listEntries.length;
                for (let x = 0; x < len; x++) {
                    if (listEntries[x]['title'] === t) {
                        id = listEntries[x]['entry_id']
                        localStorage.setItem('id', id)
                    }
                }
                return id
            }
            else if (data['Message'] === 'Token is invalid!') {
                alert('Please login first');
                window.location.href = 'index.html';
            }
        })
}

async function update_entry() {
    await return_id();
    let id = localStorage.getItem('id')
    localStorage.removeItem('id')
    fetch(url + 'api/v1/entries/' + id, {
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
    if (!id){
        return alert('No entry to delete')
    }
    localStorage.removeItem('id')
    fetch(url + 'api/v1/entries/' + id, {
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
        return window.location.href = 'home_page.html';
    }
    else if (data['Message'] != 'Entry deleted') {
        alert('No changes made');
        return window.location.href = 'home_page.html';
        }
    })
    .catch(error => console.error(error))
}

async function delete_several() {
    let result = confirm('Are you sure you want to delete')
    if (result) {
        let checked_box = document.querySelectorAll('input[type="checkbox"]')
        for (const box of checked_box) {
            if (box.checked) {
                let title = box.nextSibling.value
                localStorage.setItem('title', title)
                await return_id();
                let id = localStorage.getItem('id')
                localStorage.removeItem('id')
                fetch(url + 'api/v1/entries/' + id, {
                    method: 'DELETE',
                    mode: 'cors',
                    credentials: 'include',
                    cache: 'reload',
                    headers: {
                        'Content-Type': 'application/json',
                        'token': localStorage.getItem('token')
                    }
                }).then(Body => Body.json())
                .catch(error => console.error(error))
            }
        }
        return window.location.href = 'home_page.html';
    }
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
        fetch(url + 'api/v1/account', {
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
            alert(data['Message'])
            if (data['Message'] === 'Password has been changed') {
                alert(data['Message']);
            }
            else if (data['Message'] != 'Token is invalid!' &&
                     data['Message'] != 'Password has been changed'
                     && data['Message'] != 'Email has been changed') {
                alert('No changes made');
            }
            else if (data['Message'] === 'Token is invalid!') {
                alert('Please login first');
                window.location.href = 'index.html';
            }
    })
        .catch(error => console.error(error))
    }
    else {
        let details = form2.email.value;
        fetch(url + 'api/v1/account', {
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
            else if (data['Message'] != 'Token is invalid!' 
                    && data['Message'] != 'Email has been changed') {
                alert('No changes made');
            }
            else if (data['Message'] === 'Token is invalid!') {
                alert('Please login first');
                window.location.href = 'index.html';
            }
    })
        .catch(error => console.error(error))
    }
}

function set_reminders() {
    let boxes = document.querySelectorAll('input[type="checkbox"]')
    let notif_dict = {}
    for (const box of boxes) {
        let date = box.value
        if (box.checked) {
            notif_dict[date] = 'true'
        }
        else if (!box.checked) {
            notif_dict[date] = 'false'
        }
    }
    fetch(url + 'api/v1/account/notifications', {
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
        cache: 'reload',
        body: JSON.stringify(notif_dict),
        headers: {
            'Content-Type': 'application/json',
            'token': localStorage.getItem('token')
        }
    }).then(Body => Body.json())
    .then(data => {
        if (data['Message'] === 'Token is invalid!') {
            alert('Please login first')
            window.location.href = 'index.html'
        }
        else {
            return true
        }
    })
    .catch(error => console.error(error))
    return true
}


function display_notifications() {
    let t = document.getElementById('entries_table');
    fetch(url + 'api/v1/account/notifications', {
            method: 'GET',
            credentials: 'include',
            cache: 'reload',
            headers: {
                'Content-Type': 'application/json',
                'token': localStorage.getItem('token')
            }
        }).then(Body => Body.json())
        .then(data => {
            if (data['Message'] != 'Token is invalid!') {
                let checked_boxes = document.querySelectorAll('input[type="checkbox"]')
                let list_notifs = data['Message'];
                let dict_notifs = list_notifs[0];
                let key_s = Object.keys(dict_notifs)
                for (const key of key_s) {
                    for (const box of checked_boxes) {
                        if (box.value === key &&
                            dict_notifs[key] == true) {
                            box.checked = true;
                        }
                    }
                }
            }
            else if (data['Message'] === 'Token is invalid!') {
                alert('Please login first');
                window.location.href = 'index.html';
            }
        })
        .catch(error => console.error(error))
}
