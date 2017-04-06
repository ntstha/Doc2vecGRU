
$(document).ready(function(){
    $("#leave_review").click(function(){
        $(this).hide();
        $("#post-review-box").show();
    })

    $("#close-review-box").click(function(){
        $("#post-review-box").hide();
        $("#leave_review").show();
    })

    $("input[type='radio']").click(function(){
        rating = $(this).val();
        $("#rating").val(rating);
    })

    $("#save").click(function(){
        rating = $("#rating").val();
        review = $("#review").val();
        $.ajax({
          method: "GET",
          url: "http://localhost:8081/check",
          data: { review: ""+review, rating: ""+rating,product_id:"B00C0XVGOE" }
        })
          .done(function( msg ) {
            $(".comments").prepend("<div class='row'><div class='col-md-12'><span class='glyphicon glyphicon-star'></span><span class='glyphicon glyphicon-star'></span><span class='glyphicon glyphicon-star'></span><span class='glyphicon glyphicon-star'></span><span class='glyphicon glyphicon-star-empty'></span>"
                                            +"author"
                                            +"<span class='pull-right'>a moment ago</span>"
                                            +"<p>"+review+"</p>"
                                        +"</div>"

                                    +"</div><hr>")

            var obj = jQuery.parseJSON(msg);
            if(obj.warn==true){
                $(".modal-body").html(obj.message)
                $('#myModal').modal('show')
            }else{
                $("#rating").val("");
                $("#review").val("");
                $("#post-review-box").hide();
                $("#leave_review").show();
            }
          });

    })

    $("#dialog_submit").click(function(){
        rating = $("#rating").val();
        review = $("#review").val();
        html=""
        for(var i=1;i<=rating;i++){
            html+="<span class='glyphicon glyphicon-star'></span>"
        }
        for(var i=1;i<=5-rating;i++){
            html+="<span class='glyphicon glyphicon-star-empty'></span>"
        }
        $(".comments").prepend("<div class='row'><div class='col-md-12'>"+html
                                                    +"author"
                                                    +"<span class='pull-right'>a moment ago</span>"
                                                    +"<p>"+review+"</p>"
                                                +"</div>"

                                            +"</div><hr>")
        $('#myModal').modal('hide')
        $("#rating").val("");
        $("#review").val("");
        $("#post-review-box").hide();
        $("#leave_review").show();
    })
})
