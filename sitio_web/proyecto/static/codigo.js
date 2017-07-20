$( document ).ready(function() {

    $("#bt_offcanvas").click(function(e){
        $('.row-offcanvas').toggleClass('active')
    });
    
    /******************* OPCIONES DE BOTÓN DERECHO EN LA LISTA *******************/
    //Ocultamos el menú al cargar la página
    $("#menu").hide();
    
    //El código referente a mostrar el menú emergente se encuentra en cada modo de vista

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

    /******************* SIDEBAR *******************/

    

    /******************* VISTA DE DOCUMENTOS *******************/

    //localStorage.setItem("modo_vista", "lista");
    //localStorage.getItem("modo_vista");
    actualizaVista();
    
    $("#cambiar_vista").on("click","#vista_cuadricula", function(){
        localStorage.setItem("modo_vista", "cuadricula");
        actualizaVista();
    });

    $("#cambiar_vista").on("click","#vista_lista", function(){
        localStorage.setItem("modo_vista", "lista");
        actualizaVista();
    });

    function actualizaVista(){
        var html = "";

        if (localStorage.getItem("modo_vista") == "cuadricula"){
            html = "<span id='vista_lista' title='ver lista' class='glyphicon glyphicon-th-list'></span>";
            vistaCuadricula();
        }
        else{ 
            html = "<span id='vista_cuadricula' title='ver iconos' class='glyphicon glyphicon-th-large'></span>";
            vistaLista();
        }

        document.getElementById('cambiar_vista').innerHTML = html;
    }

    function vistaCuadricula(){
        var html = "" +
            "<div class='container-fluid cuadricula'>" +
                "<div class='row'>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_1' title='Carpeta 1'>" +
                            "<img src='/static/images/folder.png'>" +
                            "<h5>Carpeta 1</h5>" +
                        "</div>" +
                    "</div>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_2'>" +
                            "<img src='/static/images/folder.png'>" +
                            "<h5>Carpeta 2<span class='glyphicon glyphicon-star'></h5>" +
                        "</div>" +
                    "</div>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_3'>" +
                            "<img src='/static/images/folder.png'>" +
                            "<h5>Carpeta 3</h5>" +
                        "</div>" +
                    "</div>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_4'>" +
                            "<img src='/static/images/folder.png'>" +
                            "<h5>Carpeta 4</h5>" +
                        "</div>" +
                    "</div>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_5'>" +
                            "<img src='/static/images/folder.png'>" +
                            "<h5>Carpeta 5</h5>" +
                        "</div>" +
                    "</div>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_6'>" +
                            "<img src='/static/images/files_icons/icon_file_music.png'>" +
                            "<h5>cancion.mp3<span class='glyphicon glyphicon-star'></h5>" +
                        "</div>" +
                    "</div>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_7'>" +
                            "<img src='/static/images/files_icons/icon_file_img.png'>" +
                            "<h5>imagen.png</h5>" +
                        "</div>" +
                    "</div>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_8'>" +
                            "<img src='/static/images/files_icons/icon_file_txt.png'>" +
                            "<h5>documento.txt<span class='glyphicon glyphicon-star'></h5>" +
                        "</div>" +
                    "</div>" +
                    "<div id='documento_vista_cuadricula' class='col-xs-4 col-md-3 col-lg-2'>" +
                        "<div id='archivo_vista_cuadricula'>" +
                            "<img src='/static/images/files_icons/icon_file_presentation.png'>" +
                            "<h5>presentacion.ppsx</h5>" +
                        "</div>" +
                    "</div>" +
                "</div>" +
            "</div> <!--> <!-- container -->";

        document.getElementById('vista_documentos').innerHTML = html;
        
        //Mostramos el menú si hacemos click derecho con el ratón
        $("div.row div").bind("contextmenu", function(e){
            $("#menu").css({'display':'block', 'left':e.pageX, 'top':e.pageY});
            return false;
        });

        //Acción al pulsar sobre un documento
        $("#documento_vista_cuadricula div").click(function( event ) {
            alert("Fila " + this.id);
        });
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
                                        "<li><a href='#''>Compartir</a></li>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='3'>" +
                            "<td><img src='/static/images/folder_lista.png' class='img-rounded img_lista'>Carpeta<span class='glyphicon glyphicon-star'></span></td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='4'>" +
                            "<td><img src='/static/images/files_icons/icon_file_txt_lista.png' class='img-rounded img_lista'>apuntes.doc<span class='glyphicon glyphicon-star'></span></td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>cancion.mp3<span class='glyphicon glyphicon-star'></span></td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_presentation_lista.png' class='img-rounded img_lista'>presentation.ppsx</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_video_lista.png' class='img-rounded img_lista'>video.mp4</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>foto.png<span class='glyphicon glyphicon-star'></span></td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>cancion.mp3</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>cancion.mp3</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>cancion.mp3</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>cancion.mp3</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>cancion.mp3</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>cancion.mp3</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
                                        "<li><a href='#''>Copiar</a></li>" +
                                        "<li><a href='#''>Mover</a></li>" +
                                        "<li><a href='#''>Añadir a favoritos</a></li>" +
                                        "<li><a href='#'>Eliminar</a></li>" +
                                    "</ul>" +
                                "</div>" +
                            "</td>" +
                        "</tr>" +
                        "<tr id='5'>" +
                            "<td><img src='/static/images/files_icons/icon_file_music_lista.png' class='img-rounded img_lista'>cancion.mp3</td>" +
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
                                        "<li><a href='#''>Compartir</a></li>" +
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

        //Mostramos el menú si hacemos click derecho con el ratón
        $("tbody tr").bind("contextmenu", function(e){
            $("#menu").css({'display':'block', 'left':e.pageX, 'top':e.pageY});
            return false;
        });

        var bt_opciones_pulsado = 0;
        //Acción al pulsar sobre el botón de opciones en la fila
        $(".btn-group").click(function( event ) {
            bt_opciones_pulsado = 1;
        });

        //Acción al pulsar sobre una fila
        $("#tabla tr").click(function( event ) {
            event.preventDefault();
            if((!bt_opciones_pulsado) && (this.id != 0))
                alert("Fila " + this.id);
            bt_opciones_pulsado = 0;
        });
    }
    //localStorage.clear();

    /******************* MOVIMIENTO MENÚ DERECHA *******************/
    var altura = $('#bt_offcanvas').offset().top;
    $(document).scroll(function(){
        if($(window).scrollTop() > altura - 50){
            $('#bt_offcanvas').addClass('fijar_boton');
        }
        else{
            $('#bt_offcanvas').removeClass('fijar_boton');
        }
    });

    /******************* SUBIDA DE ARCHIVOS *******************/
    //Obteber datos de los archivos
    document.getElementById('upload').addEventListener('change', function(){
        var html = "";
        for(var i = 0; i<this.files.length; i++){
            var file =  this.files[i];
            html += "<p>" + file.name + "</p>";
            html += "" +
                "<div class='progress progress-striped'>" +
                    "<div class='progress-bar progress-bar-info' role='progressbar'" +
                    "aria-valuenow='20' aria-valuemin='0' aria-valuemax='100'" +
                    "style='width: 20%'>" +
                    "<span class='sr-only'>20% completado</span>" +
                    "</div>" +
                "</div>";

            //alert("name : " + file.name);
            //console.log("size : " + file.size);
            //console.log("type : " + file.type);
            //console.log("date : " + file.lastModified);
            
        }
        myFunction(html);

    }, false);

    
    //Abrir popup
    function myFunction(html) {

        html += "<button id='bt_hecho_popup' class='btn btn-primary'>Hecho</button>";
        
        popup = document.getElementById("myPopup");
        popup.innerHTML = html;
        popup.style.visibility = "visible";
        
        $(document).ready(function(){
            $("#bt_hecho_popup").click(function(){
                popup.style.visibility = "hidden";
            });
        });
    }
});