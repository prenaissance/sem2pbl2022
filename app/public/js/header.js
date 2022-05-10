window.onscroll = function showHeader() {
    var header = document.querySelector('header');

    if(window.pageYOffset > 100) {
        header.classList.add('header_fixed');
        header.classList.remove('text_shadow');
    } else {
        header.classList.remove('header_fixed');
        header.classList.add('text_shadow');
    }
}
