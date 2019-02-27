var tracker = [];
var idTracker = [];
var bigBoard = 0;
var smallBoard = 0;
var size = 0;
var width = 0;


function loadGame() {
	clear(function() {
			$("#board").empty();
		}, 3000)
        $("#board").attr("class", "hide");
        tracker = [];
        idTracker = [];

	var user = document.getElementById("user").innerHTML;
	var size = 4;
	postObj = {
		username: user,
		size: size
	};
	$.ajax({
		url: "/create_game",
		type: "POST", 
		contentType: "application/json", // type of content being sent
		dataType: "json", // type of content being received
		data: JSON.stringify(postObj), //create the specific board for a user
		success: function(data) {
					var element = document.getElementById("board");
					console.log(parseInt(size));
     				var name = 0;
     				for (var x = 0; x < (parseInt(size)) ; x++) {
						var tableRow = "row" + x;
						console.log(tableRow);
						$("#board").append("<tr id = " + tableRow + "></tr>");
						for (var y = 0; y < parseInt(size); y++) {
							$("#" + tableRow).append("<td><div value = " + x + " name =" + y + " id =" + name  + " class = 'tile'></div></td>");
							name++;
						}
					}
                    
                    element.classList.remove("hide");
					var width = document.getElementById('board').offsetWidth;
					var maxwidth = window.screen.availWidth
					var avMargin = (maxwidth - width) / 2

					$("#divW").html(width/size);

					click(data);
				}
	});
}

function clear(){
    
    	$("#board").empty();
        $("#board").attr("class", "hide");
        // $("#correct").html("");

}