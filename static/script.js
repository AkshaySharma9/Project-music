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

			// get the song id
			var song_id = $.trim(parent.children().first().attr('id'))
			console.log(liked + "  " + song_id);
			if (liked == "Like")
				liked = 2;
			else
				liked = 3;


			// send it back to server
			$.getJSON("/getFeedback",{uid:uid, s_id:song_id, feedback:liked})
		    .done(function(data, textStatus, jqXHR) {
		    	console.log("saved the feedback");
		        
		    })
		    .fail(function () {
		    	alert("Server is offline...can't save the feedback");
		    });

		});



		

		// TODO : get the new song list
	}
	else {
		$(".homepage").html("<h1>Hey welcome guest!</hr><br> Login First");
	}



	function displaySongs(song_list) {
		// TODO
		var html = "";
		for(var i = 0; song_list[i]; i++) {
			var song_box = "<div class='songbox'><div class='song' id='" + song_list[i].s_id + "'>" + song_list[i].title + "</div><div class='feedback'><span class='liked' style='float:left;'>Like</span><span class='liked' style='float:right;'>Unliked</span></div></div>";
			html += song_box;		
		}

		$(".homepage").html(html);
		
	}



});