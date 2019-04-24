'''
gives top 'n' popular songs
on basis of number of user who listened to song
'''
def popular_songs_list():
	with open ("data//popular_songs.txt", "w") as f:
		file = open('data/kaggle_visible_evaluation_triplets.txt', 'r')
		songs = dict()
		for line in file:
			user, song, count = line.strip().split('\t')
			if song in songs:
				songs[song] += 1
			else:
				songs[song] = 1
		file.close()

		# sorting the songs
		sorted_songs = sorted(songs.keys(), key = lambda x: songs[x], reverse = True)

		for song in sorted_songs:
			f.write(song + "\n")

'''
With the already sorted list of popular songs
map them to track id
'''
def map_song_to_track():
        with open ("data//popular_songs_to_track.txt", "w") as file:
                tracks = dict()
                with open("data//taste_profile_song_to_tracks.txt", "r") as f1:
                        for line in f1:
                                l,t = line.strip().split('\t')
                                if not l in tracks:
                                        tracks[l] = t
                with open("data//popular_songs.txt","r") as f2:
                        for song in f2:
                                s = song.strip()
                                if s in tracks:      
                                        file.write(s + '\t' + l[s] + '\n')
                                        break;

'''
Function to map track id to its artist and title
and save it to database
'''
def map_tracks_old():
        tracks_titles = dict()
        with open("data//unique_tracks_mapping.txt", "r") as file:
                for line in file:
                        track, song, artist, title = line.strip().split('<SEP>')
                        print(track, song, artist, title)
                        tracks_titles[song] = [artist, title]

        import sqlite3
        db = sqlite3.connect("data//database.db")

        with open("data//popular_songs.txt","r") as file:
                for line in file:
                        song = line.strip()
                        try:
                                if tracks_titles[song]:
                                        query = 'INSERT INTO tracks_details(track_id, artist, title) VALUES("{track}", "{artist}", "{title}")'.format(track = song, artist = tracks_titles[song][0], title = tracks_titles[song][1])
                                        db.execute(query)
                                        db.commit()
                        except:
                                print("ERROR: Can't find track {}".format(song))



def map_tracks():
        import csv
        tracks_titles = dict()
        with open("data//music.csv") as file:
                reader = csv.DictReader(file)
                for line in reader:
                        song, artist, title = line['song.id'], line['artist.name'], line['title']
                        print( song, artist, title)
                        tracks_titles[song] = [artist, title]

        import sqlite3
        db = sqlite3.connect("data//database.db")

        with open("data//popular_songs.txt","r") as file:
                for line in file:
                        song = line.strip()
                        try:
                                if tracks_titles[song]:
                                        query = 'INSERT INTO tracks_details(track_id, artist, title) VALUES("{track}", "{artist}", "{title}")'.format(track = song, artist = tracks_titles[song][0], title = tracks_titles[song][1])
                                        db.execute(query)
                                        db.commit()
                        except:
                                print("ERROR: Can't find track {}".format(song))


map_tracks()
