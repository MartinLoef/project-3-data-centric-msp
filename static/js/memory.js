var tracker = [];
var idTracker = [];
var bigBoard = 0;
var smallBoard = 0;
var guesses = 0;
var correct = 0;

function markPresent() {
    window.markDate = new Date();
    $(document).ready(function() {
        $("div.absent").toggleClass("present");
    });
    updateClock();
}

function updateClock() {  
    var currDate = new Date();
    var diff = currDate - markDate;
    document.getElementById("timer").innerHTML = format(diff/1000);
    setTimeout(function() {updateClock()}, 1000);
}

function format(seconds)
{
var numhours = parseInt(Math.floor(((seconds % 31536000) % 86400) / 3600),10);
var numminutes = parseInt(Math.floor((((seconds % 31536000) % 86400) % 3600) / 60),10);
var numseconds = parseInt((((seconds % 31536000) % 86400) % 3600) % 60,10);
    return ((numhours<10) ? "0" + numhours : numhours)
    + ":" + ((numminutes<10) ? "0" + numminutes : numminutes)
    + ":" + ((numseconds<10) ? "0" + numseconds : numseconds);
}
/*
	Function: Create a New Game
	 Purpose: Create a random board based on the selected boardsize
		  in: boardsize as input
*/
function loadGame() {
	clear(function() {
			$("#board").empty();
		}, 3000)
        $("#board").attr("class", "hide");
        tracker = [];
        idTracker = [];
        guesses = 0;
    
	var user = document.getElementById("user").innerHTML;
	var e = document.getElementById("BoardSize");
	var size = e.options[e.selectedIndex].value;
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
		    guesses = 0;
		    $("#guesses").html("Guesses: ");
					var element = document.getElementById("board");
					var name = 0;
     				for (var x = 0; x < (parseInt(size)) ; x++) {
						var tableRow = "row" + x;
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
					markPresent()
				}
	});
}

/*
	Function: Activate a tile and show the related value in the tile
	 Purpose: determine which tile in the board is clicked
		  in: board 
*/

function click(data) {
	var name = 0;
	for (var i = 0; i < data.board.length; i++) {
		for (var j = 0; j < data.board[i].length; j++) {
			// Selector is the element extracted using the name
			$("#" + name).click(function() {
				chosenBlock($("#" + this.id).attr("value"), $("#" + this.id).attr("name"), this.id);
			});
			name++; // incrementing name selector 
		}
	}
}

/*
	Function: Set the value to the tile based on the board
	 Purpose: determine which tile is clicked and find the related value
		  in: tile id
*/


function chosenBlock(i, j, id) {
	var obj = {};
	var user = document.getElementById("user").innerHTML;
	var e = document.getElementById("BoardSize");
	var size = e.options[e.selectedIndex].value;
	obj.row = i;
	obj.col = j;
	obj.id = id;
	postObjChoice = {
		username: user,
		choice: JSON.stringify(obj)
	}
	$.ajax({
		url: "/tile_click",
		type: "POST",
		contentType: "application/json",
		dataType: "json",
		data: JSON.stringify(postObjChoice),
		success: function(data) {
			// prevents from inputting values inside the tile once its already flipped
			if (!document.getElementById(data.id).hasChildNodes()) {
				activate(data.id, data.value);
				tracker.push(data.value);
				idTracker.push(data.id);
				guesses++;
				scan(guesses);
				currentGuesses = Math.round(guesses / 2);
				$("#guesses").html("Guesses: " + currentGuesses);
				if (tracker.length > 1) {
					if (tracker[0] !== tracker[1]) {
						deactivate(data.id); // Deactivate the current selection
						deactivate(idTracker[0]); // Deactivate the one before as well
						tracker.pop(); // Empty out the arrays to be filled with new ones
						idTracker.pop(); // Empty the id tracking array as well
						tracker.pop();
						idTracker.pop();
						scan(guesses); // scan for guesses
					}
					else {
					    correct ++;
						if ((correct == 8) && (parseInt(size) == 4)) { //winner winner chicken dinner
						    var timeElapsed = document.getElementById("timer").innerHTML
						    $("#time").html(timeElapsed)
						    $("#guesses").html("Guesses: " + currentGuesses + " in : " + timeElapsed);
						    $('#Score').removeClass('hide');

						}
						else if ((correct == 18) && (parseInt(size) == 6)){
							var timeElapsed = document.getElementById("timer").innerHTML
						    document.getElementById("timer").innerHTML = timeElapsed
							$("#guesses").html("Guesses: " + currentGuesses + " in : " + timeElapsed);
							 $("#time").html(timeElapsed)
							$('#Score').removeClass('hide');
							
						}
					}
					if (tracker[0] === tracker[1]) {
						while (tracker.length !== 0) {
							tracker.pop();
						}
						while (idTracker.length !== 0) {
							idTracker.pop();
						}
					}
				}
			}
	},
	});
}

/*
	Function: activate
	 Purpose: Flips the tile when clicked and adds a value
		  in: id, value
*/
function activate(id, value) {
	$("#" + id).attr("class", "flipped");
	var width = document.getElementById('board').offsetWidth;
	var e = document.getElementById("BoardSize");
	var size = e.options[e.selectedIndex].value;

	if (value == 1){
	    $("#" + id).append(`<i class="medium material-icons">` + "brightness_1" + `</i>`);
	} 	
	else if (value == 2){
	    $("#" + id).append(`<i class="medium material-icons">` + "brightness_2" + `</i>`);
	}
	else if (value == 3){
	    $("#" + id).append(`<i class="medium material-icons">` + "brightness_3" + `</i>`);
	}
	else if (value == 4){
	    $("#" + id).append(`<i class="medium material-icons">` + "brightness_4" + `</i>`);
	}
	else if (value == 5){
	    $("#" + id).append(`<i class="medium material-icons">` + "brightness_5" + `</i>`);
	}
	else if (value == 6){
	    $("#" + id).append(`<i class="medium material-icons">` + "brightness_6" + `</i>`);
	}
	else if (value == 7){
	    $("#" + id).append(`<i class="medium material-icons">` + "brightness_7" + `</i>`);
	}
	else if (value == 0){
	    $("#" + id).append(`<i class="medium material-icons">` + "brightness_auto" + `</i>`);
	}
	else if (value == 8){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_clear" + `</i>`);
	}
	else if (value == 9){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_bottom" + `</i>`);
	}
	else if (value == 10){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_inner" + `</i>`);
	}
	else if (value == 11){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_outer" + `</i>`);
	}
	else if (value == 12){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_left" + `</i>`);
	}
	else if (value == 13){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_right" + `</i>`);
	}
	else if (value == 14){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_horizontal" + `</i>`);
	}
	else if (value == 15){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_vertical" + `</i>`);
	}
	else if (value == 16){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_all" + `</i>`);
	}
	else if (value == 17){
	    $("#" + id).append(`<i class="medium material-icons">` + "border_top" + `</i>`);
	}
	else{
	    $("#" + id).append(`<span>` + value + `</span>`);
	}
	
	
}
/*
	Function: deactivate
	 Purpose: When clicked removes a value by removing the span and changes the physical look of the tile
		  in: id
*/
function deactivate(id) {
	window.setTimeout(function() {
		$("#" + id).attr("class", "tile");
		$("#" + id).children().remove();
	}, 800);
}
/*
	Function: scan
	 Purpose: Scans all the blocks to check if all of the blocks have been flipped
		  in: guesses 
*/
function scan(guesses) {
	var number = 0;
	var count = 0;
	// Everytime the for loop starts count gets incremented
	for (var i = 0; i < bigBoard; i++) {
		for (var j = 0; j < smallBoard; j++) {
			if (document.getElementById(number).hasChildNodes()) {
				count++;
			}
			number++;
		}
	}
	if (count === bigBoard * smallBoard) {
		var nothing = "";
		}
}

function SubmitScore(){
	var obj = {};
	var user = document.getElementById("user").innerHTML;
	var timeElapsed = document.getElementById("time").innerHTML;
	var e = document.getElementById("BoardSize");
	var size = e.options[e.selectedIndex].value;
	postObjScore = {
                    username: user,
                    size: size,
                    turns: currentGuesses,
                    time: timeElapsed
                    
                    }

	$.ajax({url: "/submitScore", type: "POST", contentType: "application/json", dataType: "json", data: JSON.stringify(postObjScore), success: function(data) {
		$("#board").empty();
		$('#Score').addClass('hide');
		$("#guesses").html("Guesses: ");
		correct = 0
	}});
}

function clear(){
    
    	$("#board").empty();
        $("#board").attr("class", "hide");
        var guesses = 0;
        var correct = 0;
        timeElapsed= 0;


}