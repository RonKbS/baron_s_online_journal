



function unveil() {
    document.getElementById('drop').classList.toggle("show");
}
window.onclick = function(event){
    if (!event.target.matches("dropped")){
        var dropdowns = this.document.getElementsByClassName("links");
        for (var i = 0; i < dropdowns.length; i++){
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')){
                    openDropDown.classList.remove('show');
                }
        }   
     }
}

/*
let c = document.getElementsByClassName('each');
let d =document.createElement('input');
d.setAttribute('type', 'checkbox');

while (true){
    c.appendChild(d);
}
*/