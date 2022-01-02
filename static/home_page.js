let cardGroups = document.querySelectorAll('.card-group');
let images = document.querySelectorAll('.card')

if($(window).width() < 992){
    for(let group of cardGroups){
        group.style.display = 'block';
    };
    for(let img of $('.card img')){
        img.style.height = '45vw';
    };
};

let x = null;
window.addEventListener('resize', () => {
    if(x == 0){
        if($(window).width() < 992){
            x = 1;
            for(let group of cardGroups){
                group.style.display = 'block';
                for(let img of $('.card img')){
                    img.style.height = '45vw';
                };
            };
        };
    } else {
        if($(window).width() >= 992) {
            x = 0;
            for(let group of cardGroups){
                group.style.display = 'flex';
                for(let img of $('.card img')){
                    img.style.height = '12vw';
                };
            };
        };
    };
});