import askvideos

# Create client
import os
api_key = os.environ.get('ASKVIDEOS_API_KEY')
client = askvideos.client.Client(api_key=api_key)

# Create an index
indices = client.list_indices()
print(indices)

index_name = 'movie_example'
if index_name not in indices['indices']:
    res = client.create_index(index_name)
    print(res)

# List all available indexes
indices = client.list_indices()
print(indices)

current_videos = client.list_videos(index_name)
print(current_videos.keys())

if 'no_country_for_old_men' not in current_videos:
    # Index a video
    movie_file = '/path/to/no_country_for_old_men/no_country_for_old_men.mp4'
    transcript_path = '/path/to/no_country_for_old_men/no_country_for_old_men.vtt'
    metadata = {
      'title': "No Country For Old Men",
      'description': "A classic thriller set in the deserts of Texas",
      'info': {}
    }
    
    results = client.index_video(
                index_name,
                video_path=movie_file,
                transcript_path=transcript_path)
    
    print(results)
    
# Search

# Search by text
# Find scenes with cowboy hats
search_term = 'cowboy hats'

results = client.search_videos(
            index_name,
            search_term,
            top_k=10)
print(results)

# Search by image
# Find scenes with an image
image_path = '/path/to/no_country_for_old_men/coin_scene.png'

results = client.search_by_image(
            index_name,
            image_path=image_path,
            top_k=10)


# Search by video
# Find scenes with an video
query_video_path = '/path/to/no_country_for_old_men/trailer.mp4'

results = client.search_by_video(
            index_name,
            video_path=query_video_path,
            start_seconds=10,
            end_seconds=14,
            top_k=10)
print(results)

# Answer Engine

# Answer a question
query = 'Which city is this movie set in?'
results = client.answer(
            index_name,
            query)
print(results)
