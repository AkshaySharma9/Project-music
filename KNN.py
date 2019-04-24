import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors


"""
This function returns the recommended songs based on the list given
and apply KNN algorithm to find more similiar songs(nearest neighbors) for each song given
"""
def getRecommendedSongs(song_list):
	# reading the dataset putting it in a dataframe
	songs = pd.read_csv('data//music.csv')

	# pre-processing the data
	df = songs.drop(['year','artist.hotttnesss','artist.id','artist.name','artist_mbtags','artist_mbtags_count','bars_confidence','bars_start','beats_start','duration','end_of_fade_in','key','key_confidence','latitude','location','longitude','mode','mode_confidence','release.id','release.name','similar','song.hotttnesss','start_of_fade_out','tatums_confidence','tatums_start','terms','terms_freq','time_signature','time_signature_confidence','title'], axis =1)
	
	song_id = songs['song.id']

	song = df.drop(['song.id'], axis = 1)


	# applying KNN alogorithm on the given dataset
	model_knn = NearestNeighbors( n_neighbors = 9)
	model_knn.fit(song.fillna(0))

	# list to store the similar songs
	predicted_songs = []

	# iterating over the songs given to function
	for songId in song_list:
		# locating the index of the song
		query_index = songs.loc[songs['song.id'] == songId].index[0]

		# getting the similar songs
		distances, indices = model_knn.kneighbors(song.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 10)

		# for each song recommended storing it in the list
		for i in range(len(distances.flatten())):
			sid  = song_id[song_id.index[indices.flatten()[i]]]
			#print('song id: '+ sid)
			#print("title: "+ (songs.loc[songs['song.id'] == song_id[song_id.index[indices.flatten()[i]]], 'title'].values)[0])
			#print((songs.loc[songs['song.id'] == song_id[song_id.index[indices.flatten()[i]]], 'artist.name'].values)[0])
			#print('------------------------')
			predicted_songs.append([song_id[song_id.index[indices.flatten()[i]]], (songs.loc[songs['song.id'] == song_id[song_id.index[indices.flatten()[i]]], 'title'].values)[0], (songs.loc[songs['song.id'] == song_id[song_id.index[indices.flatten()[i]]], 'artist.name'].values)[0], distances.flatten()[i]])

	# sorting the recommended song in ascending order of the distances
	predicted_songs.sort(key = lambda x: x[3])

	#returning the list to caller function
	return predicted_songs
