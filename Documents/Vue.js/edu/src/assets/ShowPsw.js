$(document).ready(function(){

// password toggle button
function showPassword(){
	$('.show-psw-btn').each(function(){ 
		var btn= $(this);
		btn.click(function(e){
			e.preventDefault();
			btn.siblings('input').each(function(){
				if($(this).attr('type') == 'password'){
					$(this).attr('type','text');
					$(this).closest('.password-container').find('.show-psw-btn .fa').replaceWith('<i class="fa fa-eye" aria-hidden="true"></i>');
				}
				else if($(this).attr('type') == 'text'){
					$(this).attr('type','password');
					$(this).closest('.password-container').find('.show-psw-btn .fa').replaceWith('<i class="fa fa-eye-slash" aria-hidden="true"></i>');
				}
			})	
		})
	})
}
// forgot password section script
function replaceModalContent() {
	$('.form-bottom-link').click(function (e) {
		e.preventDefault();
		$('.modal-content.signinSection').hide();
		$('.modal-content.forgot-psw').show();
	})
	$('.return-signIn-link').click(function(e){
		e.preventDefault();
		$('.modal-content.forgot-psw').hide()
		$('.modal-content.signinSection').show();
	})
}

showPassword();
replaceModalContent();	


});
