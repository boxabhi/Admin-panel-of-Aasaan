$(document).ready(function(){
	$("#owl1").owlCarousel({
		loop:true,
		margin:10,
		nav:true,
		autoplay:400,
	  responsive:{
		0:{
    		items:1
			},
		320:{
    		items:1
			},
		768:{
    		items:1
			},
		1200:{
			items:1
			}	
		}
	})
	

	$('#owl1 .item img').each(function(){
		var thumbAttr= $(this).attr('src');
		var productImg=$('.product-img.product-coat img')
		$(this).click(function(){
			productImg.attr('src',thumbAttr);
		})
	})

	$.fn.jumpToTop=function(){
 		$(this).on('click',function(){
 			$('html,body').animate({scrollTop:0},1000);
 		})

  	}

 $(".scrollbtn").jumpToTop(); 	
 
 
});

