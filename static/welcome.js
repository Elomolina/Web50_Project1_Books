let books = '';
let contador = 0;
let num = 3336;
let ultimo_libro = '';
let pp = document.getElementById("posters")
//gracias a la función de IntersectionObserver podremos crear un observador que se 
//ejecute cuando llegue al último libro de tal manera que vuelva a consumir de la api y dar la ilusión de un scroll infinito
let observador = new IntersectionObserver((entradas) => 
{
    //vigila la entrada, es decir, cuando estamos en la ultima imagen
    entradas.forEach(entrada => {
        if(entrada.isIntersecting)
        {
            num += 10;
            libro();
        }
    })
},{
    rootMargin: '0px 0px 0px',
    threshold:1.0
}
);

async function libro()
{
    entry = {"numero": num}
    //gracias al await todas las demás ejecuciones se paran hasta que realiza 
    //las que están adentro del fetch
    await fetch('/welcomeDatos', 
    {
        method:"POST",
        body:JSON.stringify(entry),
        headers:
            {
                "content-type":"application/json"
            }
        
    }).then(response => response.json())
    .then(function(data)
    {
        data.forEach(datitos =>
            books += `
        <div class="books">
        <a href="/${datitos.isbn}" target="_blank" style="text-decoration:none; color:black;"><h3 class="titulo">${datitos.titulo}</h3></a>
        <a href="/${datitos.isbn}" target="_blank"><img src="https://covers.openlibrary.org/b/isbn/${datitos.isbn}-M.jpg" alt=""></a>
        </div>`)
        
    });
    pp.innerHTML=books;
    let bookClass = document.getElementsByClassName("books");
    if(ultimo_libro)
    {
        observador.unobserve(ultimo_libro);
        //utilizamos el observador para visualizar el último elemento brindado por el fetch
    }
    ultimo_libro= bookClass[bookClass.length - 1]; 
    observador.observe(ultimo_libro);
}
libro();








//VER COMO FUNCIONA UNA HPTA APII Y LAS COOKIES
