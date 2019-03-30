$( function(){
	let file_input = $('#product_images');
	const sendImages = $('#btnSendImages');
	let mainContainer = $('#formContainer');
	
	$(mainContainer).on('change', file_input, function(){
		if (file_input.val() != "") {
			sendImages.removeClass('hidden');
		}
	});

	$(sendImages).click(function(){
		$('#formImages').submit();
		$(mainContainer).html(`
			<div class="spinner">
				<div class="double-bounce1"></div>
                <div class="double-bounce2"></div>
            </div>
			<h4 class="text-center">Please wait we are loading your images...</h4>

        `);
	});
});