$(document).ready(function() {

    function setContent(value) {
        $('#preview-content').html(marked(value));
        $('#preview-content img').each(function() {
            $(this).addClass('img-responsive');
        });
    }

    function setTitle(value) {
        $('#preview-title').text(value);
    }

    $('.comment-reply-btn').click(function(event) {
        event.preventDefault();
        $(this).parent().next('.comment-reply').fadeToggle();
    });

    $('.content-markdown').each(function() {
        var content = $(this).text();
        $(this).html(marked(content))
    });
    $('.post-detail-item img').each(function() {
        $(this).addClass('img-responsive');
    });

    var titleInput = $('#id_title');
    setTitle(titleInput.val());

    var contentInput = $('#id_content');
    setContent(contentInput.val());

    contentInput.keyup(function() {
        setContent($(this).val());
    });

    titleInput.keyup(function() {
        setTitle($(this).val());
    });

})
