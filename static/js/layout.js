$(".user").click(function(e) {
    $.post("/set_user?nombre=" + e.currentTarget.text.trim(), function() { location.reload() });
})