let contForm1 = document.getElementById("contForm1");
let contForm2 = document.getElementById("contForm2");
let buttonSiguiente = document.getElementById("buttonSiguiente");
let username = document.getElementById("username");
let h6 = document.getElementById("h6");
let h6_2 = document.getElementById("h6_2");
let nombreCompleto = document.getElementById("nombreCompleto");
let envio = document.getElementById("envio");
let password = document.getElementById("password");
let confirmPassword = document.getElementById("confirmPassword");
username.addEventListener("input", usuario);
nombreCompleto.addEventListener("input", usuario);
buttonSiguiente.addEventListener("click", botonActivado);
password.addEventListener("input", confirmation);
confirmPassword.addEventListener("input", confirmation);
username.addEventListener("keypress", 
function(event)
{
    if(event.key == "Enter")
    {
        buttonSiguiente.click();
    }
}
);

function usuario()
{
    username.value = username.value.replace(' ', '_'); //reemplaza los espacios por guiones
    if(username.value.length < 6 && username.value.length > 0)
    {
        h6.style.display = "block";
    }
    else 
    {
        h6.style.display = "none";
    }
    if(username.value.length >= 6 && nombreCompleto.value.length > 0)
    {
        buttonSiguiente.disabled = false;
    }
    else 
    {
        buttonSiguiente.disabled = true;
    }
}

function botonActivado()
{
   contForm1.style.display ="none";
   contForm2.style.display = "block";
   envio.style.display = "block";
}
function confirmation()
{
    if((password.value != confirmPassword.value) && confirmPassword.value.length > 0)
    {
        envio.disabled = true;
        h6_2.style.display = "block";
    }
    else 
    {
        if(password.value.length >=8 && password.value == confirmPassword.value)
        {
            envio.disabled = false;
            h6_2.style.display = "none";
        }
    }
}
