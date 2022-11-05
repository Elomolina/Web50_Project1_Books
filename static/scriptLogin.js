username = document.getElementById("username");
username.addEventListener("input", usuario);
function usuario()
{
    username.value = username.value.replace(' ', '_'); 
}