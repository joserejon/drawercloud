$( document ).ready(function() {

    $("#bt_offcanvas").click(function(e){
        $('.row-offcanvas').toggleClass('active')
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