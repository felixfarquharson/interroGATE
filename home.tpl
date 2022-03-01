<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h1>A suspiciously empty website.</h1>
<p></p>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js" integrity="sha512-894YE6QWD5I59HgZOGReFYm4dnWc1Qt5NtvYSaNcOP+u1T9qYdvdihz0PPSiiqn/+/3e7Jo4EaG7TubfWGUrMQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
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
        $.post("/api/poll", JSON.stringify({"id": uid}), function (data){
            $("body").text("");
            for (let i = 0; i < data["dialog"].length; i++){
                $("body").append("<div id='" + data["dialog"][i]["id"] +
                "'><h1>" + data["dialog"][i]["question"] +
                "</h1><button id='yes' onclick='yesfunc'>yes</button>" +
                "<button id='no' onclick='nofunc'>no</button></div>");
            };
        });
    };
    setInterval(poll, 1000)
</script>
</body>
</html>
