$( document ).ready(function() {

    var bt_opciones_pulsado = 0;
    //Acción al pulsar sobre el botón de opciones en la fila
    $(".btn-group").click(function( event ) {
        event.preventDefault();
        bt_opciones_pulsado = 1;
    })
    //Acción al pulsar sobre una fila
    $("#tabla tr").click(function( event ) {
        event.preventDefault();
        if((!bt_opciones_pulsado) && (this.id != 0))
            alert("Fila " + this.id);
        bt_opciones_pulsado = 0;
    })

    /******************* OPCIONES DE BOTÓN DERECHO EN LA LISTA *******************/
    //Ocultamos el menú al cargar la página
    $("#menu").hide();
    //Mostramos el menú si hacemos click derecho con el ratón
    $(document).bind("contextmenu", function(e){
        $("#menu").css({'display':'block', 'left':e.pageX, 'top':e.pageY});
        return false;
    });
    //Cuando hagamos click, el menú desaparecerá
    $(document).click(function(e){
        if(e.button == 0){
            $("#menu").css("display", "none");
        }
    });
    //Si pulsamos esc, el menú desaparecerá
    $(document).keydown(function(e){
        if(e.keyCode == 27){
            $("#menu").css("display", "none");
        }
    });
    //Acciones de los botones del menú
    $("#menu").click(function(e){
        //El switch utiliza los IDs de los <li> del menú
        switch(e.target.id){
            case "descargar":
                alert("Descargando");
                break;
            case "copiar":
                alert("Copiado");
                break;
            case "mover":
                alert("Movido");
                break;
            case "addfavoritos":
                alert("Añadido a favoritos");
                break;
            case "eliminar":
                alert("Eliminado");
                break;
        }
    });

    /******************* VISTA DE DOCUMENTOS *******************/
    $('#vista_cuadricula').click(function(event){
        event.preventDefault();
        vistaCuadricula();
    });
    $('#vista_lista').click(function(event){
        event.preventDefault();
        vistaLista();
    });

    function vistaCuadricula(){
        var html = "" +
            "<div class='container-fluid cuadricula'>" +
                "<div class='row'>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2' title='Donec id elit non mi porta gravida at eget metusDonec id elit non mi porta gravida at eget metusDonec id elit non mi porta gravida at eget metusDonec id elit non mi porta gravida at eget metusDonec id elit non mi porta gravida at eget metus'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Donec id elit non mi porta gravida at eget metusDonec id elit non mi porta gravida at eget metusDonec id elit non mi porta gravida at eget metusDonec id elit non mi porta gravida at eget metusDonec id elit non mi porta gravida at eget metus</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Nombre archivo</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Donec id elit non mi porta gravida at eget metus</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Nombre archivo</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Donec id elit non mi porta gravida at eget metus</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Nombre archivo</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Donec id elit non mi porta gravida at eget metus</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Nombre archivo</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Donec id elit non mi porta gravida at eget metus</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Nombre archivo</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Donec id elit non mi porta gravida at eget metus</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Nombre archivo</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Donec id elit non mi porta gravida at eget metus</h5>" +
                    "</div>" +
                    "<div id='archivo_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<img src='/static/images/folder.png'>" +
                        "<h5>Nombre archivo</h5>" +
                    "</div>" +
                "</div>" +
            "</div> <!--> <!-- container -->";

        document.getElementById('vista_documentos').innerHTML = html;
    }

    function vistaLista(){
        var html = "" +
            "<div class='table-responsive'>" +
                "<table id='tabla' class='table'>" +
                    "<thead>" +
                        "<tr>" +
                            "<th>Nombre archivo</th>" +
                            "<th>Tamaño</th>" +
                            "<th>Última modificación</th>" +
                            "<th>Disponible para</th>" +
                            "<th class='hidden-xs'>Opciones</th>" +
                        "</tr>" +
                    "</thead>" +
                    "<tbody>" +
                        "<tr id='1'>" +
                            "<td><img src='/static/images/folder_lista.png' class='img-rounded img_lista'>Carpeta</td>" +
                            "<td class='center'>1GB</td>" +
                            "<td class='center'>07/04/2017</td>" +
                            "<td class='center'>Solo yo</td>" +
                            "<td class='hidden-xs'>" +
                                "<div class='btn-group'>" +
                                    "<button type='button' class='btn btn-info dropdown-toggle' data-toggle='dropdown'>" +
                                    "Más <span class='caret'></span>" +
                                    "</button>" +
                                    "<ul class='dropdown-menu' role='menu'>" +
                                        "<li><a href='#''>Descargar</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='2'>" +
                            "<td><img src='/static/images/folder_lista.png' class='img-rounded img_lista'>Carpeta</td>" +
                            "<td class='center'>1GB</td>" +
                            "<td class='center'>07/04/2017</td>" +
                            "<td class='center'>Solo yo</td>" +
                            "<td class='hidden-xs'>" +
                                "<div class='btn-group'>" +
                                    "<button type='button' class='btn btn-info dropdown-toggle' data-toggle='dropdown'>" +
                                    "Más <span class='caret'></span>" +
                                    "</button>" +
                                    "<ul class='dropdown-menu' role='menu'>" +
                                        "<li><a href='#''>Descargar</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='3'>" +
                            "<td><img src='/static/images/folder_lista.png' class='img-rounded img_lista'>Carpeta</td>" +
                            "<td class='center'>1GB</td>" +
                            "<td class='center'>07/04/2017</td>" +
                            "<td class='center'>Solo yo</td>" +
                            "<td class='hidden-xs'>" +
                                "<div class='btn-group'>" +
                                    "<button type='button' class='btn btn-info dropdown-toggle' data-toggle='dropdown'>" +
                                    "Más <span class='caret'></span>" +
                                    "</button>" +
                                    "<ul class='dropdown-menu' role='menu'>" +
                                        "<li><a href='#''>Descargar</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                    "</tbody>" +
                "</table>" +
            "</div> <!-- table-responsive -->";

        document.getElementById('vista_documentos').innerHTML = html;
    }
});