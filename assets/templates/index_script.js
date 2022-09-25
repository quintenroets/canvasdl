onload = function() {
    let opened = false;
    var links = document.getElementsByTagName('a');
    let toOpen = "";
    let staticOpen = false;
    let index_id = window.location.href;
    
    url = window.localStorage.getItem(index_id);
    if (url){
        let id = 'school-position-' + url + "done";
        let done = window.localStorage.getItem(id);
        if (url && url.includes("/")){
            if (done !== "true"){
                toOpen = url;
                staticOpen = true;
                opened = true;
            }
        }
    }
    
    for(var i = 0; i< links.length; i++){
        let id = 'school-position-' + links[i].href + "done";
        let done = window.localStorage.getItem(id);
        let href = links[i].href;
        links[i].addEventListener('click', function(){
            onClick(href);
        });
        
        if (done !== "true" && opened == false){
            toOpen = links[i].href;
            opened = true;
        }
    }
    if (toOpen){
        let tab = window.open(toOpen,'_blank');
        tab.focus();
    }
    
    buttons = document.getElementsByTagName('button');
    for(var j = 0; j< buttons.length; j++){
        let href = links[j].href
        buttons[j].addEventListener('click', function(){
            buttonOnClick(href);
        });
    }
    setColors();
    
}

setColors = function() {
    var links = document.getElementsByTagName('a');
    for(var i = 0; i< links.length; i++){
        let id = 'school-position-' + links[i].href + "done";
        let done = window.localStorage.getItem(id);
        var color;
        
        if (done !== "true"){
            color = "#949CA5";
        } else if (done == "true"){
            color = "#1b59A8";
        }
        links[i].style.color = color;
    }
}

window.onload = onload;

onClick = function(href) {
    let index_id = window.location.href;
    let url = href;
    window.localStorage.setItem(index_id, url);
}

buttonOnClick = function(href) {
    let id = 'school-position-' + href;
    let id_done = id + 'done';
    let done_value = window.localStorage.getItem(id_done);
    var new_done_value;
    if (done_value === "true") {
        new_done_value = false;
    } else {
        new_done_value = true;
    }
    window.localStorage.setItem(id_done, new_done_value);
    setColors();
}
