let input = document.getElementById("barra");
let posters = document.getElementById("posters");
let p = '';
input.addEventListener("input", inputs);
let datitos2;
let opcion = document.getElementById("select")
opcion.addEventListener("change", inputs)
async function inputs()
{
    p='';
    let indice = opcion.selectedIndex;
    if(indice)
    {
        input.disabled = false;
    }
    if(input.value.length > 0)
    {
        let informacion = {value:input.value, option:opcion[indice].text};
        await fetch('/libros',
        {
            method:"POST", 
            body: JSON.stringify(informacion),
            headers:{"content-type":"application/json"}
        }).then(response => response.json()).then(function(data)
        {
            datitos2 = data;
        })
        p = '';
        datitos2.forEach(datitos => 
            p += `
        <div class="books">
        <a href="/${datitos.isbn}" target="_blank" style="text-decoration:none; color:black">    <h3 class="titulo">${datitos.titulo}</h3></a>
        <a href="/${datitos.isbn}" target="_blank"><img src="https://covers.openlibrary.org/b/isbn/${datitos.isbn}-M.jpg" alt=""></a>
        </div>`);
        posters.innerHTML= p;
    }

}