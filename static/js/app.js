/**
 * Función que responde al evento chage del
 * campo fileFoto y muestra la foto seleccionada
 * en un elemento de tipo image del formulario 
 * llamado imagenProducto
 * @param {*} evento
 */

function visualizarFoto(evento) {
    $fileFoto = document.querySelector('#fileFoto')
    $imagenPrevisualizacion = document.querySelector("#imagenProducto")
    const files = evento.files
    const archivo = files[0]
    let filename = archivo.filename
    let extension = filename.split('.').pop()
    extension = extension.toLowerCase()
    
    if(extension !== 'jpg') {
        $fileFoto.value = ''
        alert('La imagen debe ser en formato JPG')
    } else {
        const objectURL = URL.createObjectURL(archivo)
        $imagenPrevisualizacion.src = objectURL
    }
}