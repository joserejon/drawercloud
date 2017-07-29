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

});