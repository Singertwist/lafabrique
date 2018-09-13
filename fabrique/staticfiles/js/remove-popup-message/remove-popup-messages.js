(function($){

	$(".popup-messages a").click(function() {
		$(this).closest('.popup-messages-overlay').remove();
	});

})(jQuery);