$(document).ready(function () { 
	var uid = '';
	$("#logi").click (function () {
		$('#login').modal();		
		
	});

	// if the user is logged in show the music list
	console.log($("#logged").length);
	if ($("#logged").length) {
		uid = $("#logged").html();
		console.log('uid=' + uid);
		// get the song list
		var songs;
		$(".homepage").html("<img alt='loading' src='/static/ajax-loader.gif'/>");
		$.getJSON("/getSonglist",{uid:uid})
		    .done(function(data, textStatus, jqXHR) {
		    	console.log(data);

		    	// display the song list to user
		       	displaySongs(data);
		        
		    })
		    .fail(function () {
		    	alert("Server is offline");
		    });


		

		// get user response on song
		$(".homepage").on("click", ".liked", function () {

			var parent = $(this).parent().parent();
			//console.log(parent.children().first());
			//console.log($.trim(parent.children().first().text()));
			//console.log($.trim(parent.children().first().attr('id')));
			
			var liked = $(this).text();

			

			// get the song id and changing the text for user
			var song_id = $.trim(parent.children().first().attr('id'))
			console.log(liked + "  " + song_id);
			if (liked == "Like") {
				liked = 3;
				$(this).text("Liked!");
				$(this).toggleClass('liked like');
			}
			else if (liked == "Unlike"){
				liked = 2;
				$(this).text("Unliked");
				$(this).toggleClass('liked unlike');
			}


			// send it back to server
			console.log(uid, song_id, liked)
			$.getJSON("/getFeedback",{uid:uid, s_id:song_id, feedback:liked})
		    .done(function(data, textStatus, jqXHR) {
		    	console.log(data);
		    	alert("You feedback for '" + $.trim(parent.children().first().text()) + "' is saved!");
		        
		    })
		    .fail(function () {
		    	alert("Server is offline...can't save the feedback");
		    });

		});

	}
	else {
		$(".homepage").html("<div id = 'intro'><h1>Hey There!</hr><br>Here you will get personalized playlist for you.<br>We have used dataset of 'Million Song Dataset' Challenge and <br> exploited it with machine learning to show you some relevant songs <br> that you may like and if not give feedback<br><br> To Continue, Login First</div>");
	}


	/*
	* Displays the song list to user
	*/
	function displaySongs(song_list) {
		var html = "";
		for(var i = 0; song_list[i]; i++) {
			var song_box = "<div class='songbox'><div class='song' id='" + song_list[i].s_id + "'>" + song_list[i].title + "<br><span class = 'artist'>" + song_list[i].artist + "</span>" +"</div><div class='feedback'><span class='liked' style='float:left;'>Like</span><span class='liked' style='float:right;'>Unlike</span></div></div>";
			html += song_box;		
		}
		$(".homepage").html(html);
		
		html = "<span id='last' style='color:white;'>You have reached the end of list, Refresh the page to see more new Songs.</span>"

		$(".homepage").append(html);
	}



});