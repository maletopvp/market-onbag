//carregando do loading até a pagina estar totalmente carregada
$(window).on('load', function () {
    $('#preloader').delay(350).addClass('fadeOut animated'); 
    $('body').delay(350).css({'overflow': 'visible'});
    setTimeout(() => {
        $('#preloader').css('display', 'none');
    }, 350);
    $('section.container').addClass('zoomIn animated');
});