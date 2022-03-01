<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>A suspiciously empty website.</h1>
<p></p>

<script src="https://code.jquery.com/jquery-3.6.0.slim.min.js"></script>
<script>
    var uid = null;
    var yesfunc = function (){
        $.post("/api/submit", {"id": $("p").text, "value": true});
    }
    var nofunc = function (){
        $.post("/api/submit", {"id": $("p").text, "value": false});
    }

    $.get("/api/init", function(data){
        uid = data["id"];
    });

    var poll = function (){
        $.post("/api/poll", {"id": uid}, function (data){
            $("body").append("<div id='" + data["id"] + "'><h1>"+data+"</h1><button id='yes' onclick='yesfunc'>yes</button>" +
                "<button id='no' onclick='nofunc'>no</button></div>");
        });
    };
    setInterval(poll, 100)
</script>
</body>
</html>