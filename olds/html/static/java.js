function suma (neme, contra) {
    var neme = document.getElementById("nombre").value;
    var contra = document.getElementById("pass").value;
    
    if (contra == "123"){
        alert ("bienvenido"+" "+neme);
    }
    else{
        alert ("contrasena incorrecta");
    }
    
    return neme;
}
