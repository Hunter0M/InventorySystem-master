



// Get the current hour (0-23)
const currentHour = new Date().getHours();

// Check if it's morning (6:00 - 11:59) or evening (18:00 - 23:59)
if (currentHour >= 6 && currentHour < 12) {
  document.body.classList.remove('evening-mode');
  document.body.classList.add('morning-mode');
} else if (currentHour >= 18 && currentHour <= 23) {
  document.body.classList.remove('morning-mode');
  document.body.classList.add('evening-mode');
}


let calcScrollValue = () => {
    let scrollProgress = document.getElementById("progress");
    let progressValue = document.getElementById("progress-value"); 
    let pos = document.documentElement.scrollTop;
    let calcHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight; 
    let scrollValue = Math.round((pos * 100) / calcHeight); 

    if (pos > 100) {
        scrollProgress.style.display = "grid";
    } else {
        scrollProgress.style.display = "none";
    } 
    scrollProgress.addEventListener("click", () => {
        document.documentElement.scrollTop = 0;
    }); 
    scrollProgress.style.background = `conic-gradient(#03cc65 ${scrollValue}%, #d7d7d7 ${scrollValue})`;

    
}

window.onscrollend = calcScrollValue;
window.onload = calcScrollValue;


(function ($) {
    "use strict";

    // Spinner
// var spinner = function () {
//     setTimeout(function () {
//         if ($('#spinner').length > 0) {
//             $('#spinner').removeClass('show');
//         }
//     }, 1);
// };
// spinner()

  // Spinner
  var spinner = function () {
    setTimeout(function () {
        if ($('#spinner').length > 0) {
            $('#spinner').removeClass('show');
        }
    }, 1);
};
spinner(0);

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });

    $('.login-reg-panel input[type="radio"]').on('change', function () {
        if ($('#log-login-show').is(':checked')) {
            $('.register-info-box').fadeOut();
            $('.login-info-box').fadeIn();

            $('.white-panel').addClass('right-log');
            $('.register-show').addClass('show-log-panel');
            $('.login-show').removeClass('show-log-panel');

        }
        else if ($('#log-reg-show').is(':checked')) {
            $('.register-info-box').fadeIn();
            $('.login-info-box').fadeOut();

            $('.white-panel').removeClass('right-log');

            $('.login-show').addClass('show-log-panel');
            $('.register-show').removeClass('show-log-panel');
        }
    });

     // Back to top button
    


    // Back to top button
//    $(window).scroll(function () {
//     if ($(this).scrollTop() > 300) {
//         $('.back-to-top').fadeIn('slow');
//     } else {
//         $('.back-to-top').fadeOut('slow');
//     }
//     });
//     $('.back-to-top').click(function () {
//         $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
//         return false;
//     }); 


    // Back to top button
    // $(window).scroll(function () {
    //     if ($(this).scrollTop() > 300) {
    //         $('.back-to-top').fadeIn('slow');
    //     } else {
    //         $('.back-to-top').fadeOut('slow');
    //     }
    // });
    // $('.back-to-top').click(function () {
    //     $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
    //     return false;
    // });

    




})(jQuery);















