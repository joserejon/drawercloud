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
        for(var i = 0; i < this.files.length; i++){
            var file = this.files[i];
            html += "" +
                "<div id='contenido_popup'" +
                    "<p>" + file.name + "</p>" +
                    "<div id='barra_progreso' class='progress progress-striped'>" +
                        "<div class='progress-bar progress-bar-info' role='progressbar'" +
                        "aria-valuenow='20' aria-valuemin='0' aria-valuemax='100'" +
                        "style='width: 20%'>" +
                        "<span class='sr-only'>20% completado</span>" +
                        "</div>" +
                    "</div>" +
                "</div>";

            subirArchivo(file.name);
            //alert("name : " + file.name);
            //console.log("size : " + file.size);
            //console.log("type : " + file.type);
            //console.log("date : " + file.lastModified);
            
        }
        //funcionPopUp(html, this.files);

    }, false);

    
    //Abrir popup
    function funcionPopUp(html, files) {

        html += "<button id='bt_hecho_popup' class='btn btn-default'>Hecho</button>";
        
        popup = document.getElementById("div_popup");
        popup.innerHTML = html;
        popup.style.visibility = "visible";
        
        $(document).ready(function(){
            $("#bt_hecho_popup").click(function(){
                popup.style.visibility = "hidden";
            });
        });

    }

    function subirArchivo(_filename) {
        $.ajax({
            url : "subidaArchivo",
            data : {
                filename: _filename
            },
            type : 'GET',
            dataType: 'json',
            success : function(datos){
                alert(datos);
            },
            failure : function(datos){
                alert('Error: no se pudo subir el archivo');
            },
            complete : function(datos) {
                console.log('Archivo subido');
            }
        });
    }
});