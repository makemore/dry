$(document).ready(function () {
    var galleryView = $(".gallery-view");

    if (galleryView.length > 0) {
        var image = $(".gallery-view img");
        var imageHeight = image.height();
        var windowHeight = $(window).height();
        var poetryHeight = $(".poetry").height();
        var galleryNavHeight = $(".gallery-nav").height();
        console.log(imageHeight, poetryHeight, galleryNavHeight, windowHeight);

        var overflow = windowHeight - (imageHeight + galleryNavHeight + poetryHeight);

        console.log(overflow);

        if ((imageHeight + galleryNavHeight + poetryHeight) > windowHeight) {
            image.height(image.height() + overflow);
        }

        $(".poetry").css("width", image.width());
    }
});