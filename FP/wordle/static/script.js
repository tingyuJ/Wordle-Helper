$(document).ready(function(){
    $('input').keyup(function(){
        this.value = this.value.toUpperCase();
        if(this.value.length==1){
            $(this).next().focus();
        }
    });
});