
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
        document.getElementById('menu-inicio').outerHTML
            =this.responseText;
    }
}
xhttp.open('GET' ,"navegadorIni.html",true);
xhttp.send();