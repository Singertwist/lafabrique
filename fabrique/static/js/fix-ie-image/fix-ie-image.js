(function($){

	$('.image-article-selection-plat img').each(function(){           // Note: {.post-thumb img} is css selector of the image tag
	    var t = $(this),
	        s = 'url(' + t.attr('src') + ')',
	        p = t.parent(),
	        d = $('<div></div>');
	    t.hide();
	    p.append(d);
	    d.css({
	        'height'                : 250,          // Note: You can change it for your needs
	        'background-size'       : 'cover',
	        'background-repeat'     : 'no-repeat',
	        'background-position'   : 'center',
	        'border-radius'			: "10px 10px 0px 0px", 
	        'background-image'      : s
	    });
	});

})(jQuery);