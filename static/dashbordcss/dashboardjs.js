
window.addEventListener('scroll', function() {
    const nav = document.querySelector('.top-menu');
    if (window.scrollY > 50) {
        nav.classList.add('active');
    } else {
        nav.classList.remove('active');
    }
});

window.addEventListener('scroll', slide);
function slide(){
    var reavels = document.querySelectorAll('.slidetop');
    
    for(var i = 0; i < reavels.length; i++){

        var windowheight = window.innerHeight;
        var reaveltop = reavels[i].getBoundingClientRect().top;
        var reavelpoint = 60;

        if(reaveltop < windowheight - reavelpoint){
            reavels[i].classList.add('active');
        }
        else{
            reavels[i].classList.remove('active');
        }
    }
}

window.addEventListener('scroll', leftslide);
function leftslide(){
    var reavels = document.querySelectorAll('.slideleft');
    
    for(var i = 0; i < reavels.length; i++){

        var windowheight = window.innerHeight;
        var reaveltop = reavels[i].getBoundingClientRect().top;
        var reavelpoint = 10;

        if(reaveltop < windowheight - reavelpoint){
            reavels[i].classList.add('active');
        }
        else{
            reavels[i].classList.remove('active');
        }
    }
}

window.addEventListener('scroll', zoomIn);
function zoomIn(){
    var reavels = document.querySelectorAll('.zoom-in');
    
    for(var i = 0; i < reavels.length; i++){
        var windowheight = window.innerHeight;
        var reaveltop = reavels[i].getBoundingClientRect().top;
        var reavelpoint = 0;

        if(reaveltop < windowheight - reavelpoint){
            reavels[i].classList.add('active');
        }
        else{
            reavels[i].classList.remove('active');
        }
    }
}


// for showing and hiding menu on small screens
// this 
function nav() {
    const bar = document.querySelector('.menu-bar');
    const menu = document.querySelector('.one-quater');
    const mediaMenu = document.querySelector('.media-menu');
    bar.addEventListener('click', () => { 
        mediaMenu.classList.toggle('active');
        menu.classList.toggle('active');
        console.log(menu.classList.contains('active') ? "menu opened" : "menu closed"); 
    });
}nav();

// or
// const nav = document.querySelector('.bar'); 
// const menu = document.querySelector('.one-quater'); 
// nav.addEventListener('click', () => { 
//     menu.classList.toggle('active'); 
//     console.log(menu.classList.contains('active') ? "menu opened" : "menu closed"); 
// });

// for showing and hidding password
function setupPasswordToggles() {
    const toggles = document.querySelectorAll('.toggle')
    toggles.forEach(toggle => {
        const passInput = toggle.previousElementSibling // the <input> before the icon

        toggle.addEventListener('click', () => {
            if (passInput.type === 'password') {
                passInput.type = 'text'
                toggle.classList.remove('fa-eye')
                toggle.classList.add('fa-eye-slash')
                console.log('password showing')
            } else {
                passInput.type = 'password'
                toggle.classList.remove('fa-eye-slash')
                toggle.classList.add('fa-eye')
                console.log('password hidden')
            }
        })
    })
}
document.addEventListener('DOMContentLoaded', setupPasswordToggles);

