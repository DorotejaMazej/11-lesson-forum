$(document).ready(function(){
    $('button').click(function(){
    var input = $('input[name=Insert sum...]').val();

    if(var input === "10"){
        $('button').hide();
        $('#check-human').hide();
    }else{
        $('button').click(function(event){
            event.preventDefault();
            $('button').appendTo("#topic-button");
        })
    }
    });
});