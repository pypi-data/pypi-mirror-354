"""
AskVideos API Client Library

This client library provides a Python interface to the AskVideos API.
It allows users to create and manage video and image indices, search through
media content using text or visual queries, and get AI-powered answers about
media content.

Usage:
    client = Client(api_key, api_url)
    index_name = "my_index"
    client.create_index(index_name)
    client.index_video(index_name, video_url="https://example.com/video.mp4")
    results = client.search_videos(index_name, "people walking")
"""

import requests
import json
import time
import os
from typing import List, Dict, Optional, Union, Any

class Client:
    def __init__(self, api_key, api_url='http://api.askvideos.com:8123'):
        """
        Initialize the client with the given API URL and API key.

        Parameters:
        api_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {"X-API-Key": self.api_key}

    def create_index(self, index_name: str, video_model_name: Optional[str] = None) -> Dict:
        """
        Create a new index with the specified name.

        Parameters:
        index_name (str): The name of the index to be created.
        video_model_name (str, optional): The name of the video model to use. Default is None.

        Returns:
        dict: JSON response indicating success or failure.
        """
        url = f"{self.api_url}/index"
        params = {"index_name": index_name}
        if video_model_name:
            params["video_model_name"] = video_model_name
        response = requests.post(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_indices(self) -> Dict:
        """
        List all indices.

        Returns:
        dict: JSON response with the current list of indices.
        """
        url = f"{self.api_url}/index"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_index(self, index_name: str) -> Dict:
        """
        Delete an index with the specified name.

        Parameters:
        index_name (str): The name of the index to be deleted.

        Returns:
        dict: JSON response indicating success or failure.
        """
        url = f"{self.api_url}/index"
        params = {"index_name": index_name}
        response = requests.delete(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_videos(self, 
                     index_name: str, 
                     query: str, 
                     asset_ids: Optional[List[str]] = None, 
                     top_k: int = 30, 
                     top_p: float = 0, 
                     modes: List[str] = ["video", "image"], 
                     queue_job: bool = False, 
                     use_masks: bool = False, 
                     use_boxes: bool = False, 
                     wait_for_result: bool = False) -> Dict:
        """
        Search for videos in the specified index using a query.

        Parameters:
        index_name (str): The name of the index to search in.
        query (str): The search query.
        asset_ids (list): List of asset ids to include search through.
        top_k (int): The number of top results to return. Default is 30.
        top_p (float): The confidence threshold for scores. Default is 0.
        modes(list): Type of asset to search for (either video or image).
        queue_job (bool, optional): Whether to queue the search task in the background. Default is False.
        use_masks (bool, optional): Whether to include mask-based segmentation in the search. Default is False.
        use_boxes (bool, optional): Whether to include box-based object detection in the search. Default is False.
        wait_for_result (bool, optional): Whether to wait for the job result if queued. Default is False.

        Returns:
        dict: JSON response containing the search results or job ID.
        """
        url = f"{self.api_url}/index/{index_name}/search"
        body = {
            "query": query,
            "top_k": top_k,
            "top_p": top_p,
            "modes": modes,
            "queue_job": queue_job,
            "use_masks": use_masks,
            "use_boxes": use_boxes,
        }
        if asset_ids:
            body["asset_ids"] = asset_ids
        response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        result = response.json()

        if queue_job:
            job_id = result.get("job_id")
            if not job_id:
                raise ValueError("Job ID not returned for queued job.")

            if wait_for_result:
                # Busy wait for the job to complete
                while True:
                    job_result = self.get_job_result(job_id)
                    status = job_result.get("status")
                    if status == "completed":
                        return job_result
                    elif status == "not_found":
                        raise RuntimeError(f"Job ID {job_id} not found.")
                    elif status == "failed":
                        raise RuntimeError(f"Job ID {job_id} failed.")
                    time.sleep(2)  # Poll every 2 seconds
            else:
                # Return the job ID if not waiting for result
                return {"job_id": job_id}

        return result

    def get_job_result(self, job_id: str) -> Dict:
        """
        Retrieve the result of a background search task.

        Parameters:
        job_id (str): The ID of the job.

        Returns:
        dict: JSON response containing the job status and results, if available.
        """
        url = f"{self.api_url}/job/result"
        params = {"job_id": job_id}
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_by_image(self, 
                       index_name: str, 
                       image_path: str, 
                       asset_ids: Optional[List[str]] = None,
                       modes: List[str] = ["video", "image"],
                       top_k: int = 30) -> Dict:
        """
        Search for videos using an image in the specified index.

        Parameters:
        index_name (str): The name of the index to search in.
        image_path (str): The local file path to the image.
        asset_ids (list, optional): List of asset ids to include in search.
        modes (list): Type of asset to search for (either video or image).
        top_k (int): The number of top results to return. Default is 30.

        Returns:
        dict: JSON response containing the search results.
        """
        url = f"{self.api_url}/index/{index_name}/search_image"
        with open(image_path, "rb") as image_file:
            files = {"image_file": image_file}
            params = {"top_k": top_k}
            data = {}
            if asset_ids:
                data["asset_ids"] = asset_ids
            if modes:
                data["modes"] = modes
            response = requests.post(url, files=files, data=data, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_by_video(self, 
                       index_name: str, 
                       video_paths: Union[str, List[str]], 
                       query_asset_ids: Optional[List[str]] = None,
                       asset_ids: Optional[List[str]] = None,
                       modes: List[str] = ["video", "image"],
                       top_k: int = 30,
                       video_multiquery_mode: str = "merge_scores_mean",
                       start_seconds: Optional[List[int]] = None,
                       end_seconds: Optional[List[int]] = None) -> Dict:
        """
        Search for videos using a video in the specified index.

        Parameters:
        index_name (str): The name of the index to search in.
        video_paths (str or list): The local file path(s) to the video(s).
        query_asset_ids (list, optional): List of existing Video IDs or Image IDs to use as queries.
        asset_ids (list, optional): List of asset ids to include in search.
        modes (list): Type of asset to search for (either video or image).
        top_k (int): The number of top results to return. Default is 30.
        video_multiquery_mode (str): Algorithm to use when multiple query videos are provided.
        start_seconds (list, optional): List of start times in seconds for each video.
        end_seconds (list, optional): List of end times in seconds for each video.

        Returns:
        dict: JSON response containing the search results.
        """
        url = f"{self.api_url}/index/{index_name}/search_video"
        
        # Convert single video to list for consistent handling
        if isinstance(video_paths, str):
            video_paths = [video_paths]
            if start_seconds is None:
                start_seconds = [0]
            if end_seconds is None:
                end_seconds = [-1]
        else:
            if start_seconds is None:
                start_seconds = [0] * len(video_paths)
            if end_seconds is None:
                end_seconds = [-1] * len(video_paths)
                
        # Validate parameters
        if len(start_seconds) != len(end_seconds) or (len(video_paths) > 0 and len(start_seconds) != len(video_paths)):
            raise ValueError("start_seconds, end_seconds, and video_paths must have the same length")
            
        files = {}
        for i, video_path in enumerate(video_paths):
            files[f"video_files"] = (f"video_{i}.mp4", open(video_path, "rb"))
            
        data = {
            "top_k": top_k,
            "video_multiquery_mode": video_multiquery_mode,
            "modes": modes
        }
        
        # Add optional parameters
        if asset_ids:
            data["asset_ids"] = ",".join(asset_ids)
        if query_asset_ids:
            data["query_asset_ids"] = ",".join(query_asset_ids)
        if start_seconds:
            for i, val in enumerate(start_seconds):
                data[f"start_seconds"] = val
        if end_seconds:
            for i, val in enumerate(end_seconds):
                data[f"end_seconds"] = val
                
        response = requests.post(url, files=files, data=data, headers=self.headers)
        response.raise_for_status()
        
        # Close all file handles
        for file_obj in files.values():
            if hasattr(file_obj[1], 'close'):
                file_obj[1].close()
                
        return response.json()

    def answer(self, 
              index_name: str, 
              query: str, 
              mode: str = 'rag', 
              video_ids: List[str] = [], 
              system_prompt: Optional[str] = None, 
              use_markdown: bool = False) -> Dict:
        """
        Get an answer for a query using the specified index and optional parameters.

        Parameters:
        index_name (str): The name of the index to use.
        query (str): The query to answer.
        mode (str): The mode of the answer, default is 'rag'. Available options: ['all', 'rag']
        video_ids (list): List of video IDs to restrict the answer to. Default uses all videos in the index.
        system_prompt (str): Optional system prompt for additional context.
        use_markdown (bool): Whether to use markdown in the response. Default is False.

        Returns:
        dict: JSON response containing the answer.
        """
        url = f"{self.api_url}/index/{index_name}/answer"
        params = {
            "query": query,
            "mode": mode,
            "use_markdown": use_markdown
        }
        if system_prompt:
            params['system_prompt'] = system_prompt
        if video_ids and len(video_ids) > 0:
            params['video_ids'] = ','.join(video_ids)
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def answer_vqa(self, 
                  index_name: str, 
                  query: str, 
                  search_term: str, 
                  asset_ids: Optional[List[str]] = None, 
                  mode: str = 'rag', 
                  system_prompt: Optional[str] = None, 
                  use_markdown: bool = True, 
                  top_p: float = 0) -> Dict:
        """
        Get an answer to a visual query using the specified index and additional search parameters.

        Parameters:
        index_name (str): The name of the index to use.
        query (str): The query to answer.
        search_term (str): The search term used for retrieval-augmented generation (RAG).
        asset_ids (list, optional): List of asset IDs to restrict the answer to. Default is None.
        mode (str, optional): The mode of answering, default is 'rag'.
        system_prompt (str, optional): Optional system prompt for context. Default is None.
        use_markdown (bool, optional): Whether to use markdown in the response. Default is True.
        top_p (float, optional): Threshold for top-p sampling. Default is 0.

        Returns:
        dict: JSON response containing the answer.
        """
        url = f"{self.api_url}/index/{index_name}/answer_vqa"
        params = {
            "query": query,
            "search_term": search_term,
            "mode": mode,
            "use_markdown": use_markdown,
            "top_p": top_p,
        }
        if system_prompt:
            params["system_prompt"] = system_prompt
        if asset_ids:
            params["asset_ids"] = ",".join(asset_ids)
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def answer_vqa_video_snippet(self, 
                                index_name: str, 
                                video_id: str, 
                                query: str, 
                                start_seconds: int = 0, 
                                end_seconds: int = -1, 
                                system_prompt: Optional[str] = None, 
                                use_markdown: bool = True) -> Dict:
        """
        Get an answer to a visual query for a specific video snippet using the specified index.

        Parameters:
        index_name (str): The name of the index to use.
        video_id (str): The ID of the video to query.
        query (str): The query to answer.
        start_seconds (int, optional): Start time of the snippet in seconds. Default is 0.
        end_seconds (int, optional): End time of the snippet in seconds. Default is -1, which indicates the end of the video.
        system_prompt (str, optional): Optional system prompt for additional context. Default is None.
        use_markdown (bool, optional): Whether to use markdown in the response. Default is True.

        Returns:
        dict: JSON response containing the answer.
        """
        url = f"{self.api_url}/index/{index_name}/{video_id}/answer_vqa"
        params = {
            "query": query,
            "use_markdown": use_markdown,
            "start_seconds": start_seconds,
            "end_seconds": end_seconds,
        }
        if system_prompt:
            params["system_prompt"] = system_prompt
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_from_youtube_search(self, 
                                 index_name: str, 
                                 search_term: str, 
                                 max_videos: int = 10, 
                                 max_duration: int = 600) -> Dict:
        """
        Index videos from a YouTube search query.

        Parameters:
        index_name (str): The name of the index to add the videos to.
        search_term (str): The search term to use for finding videos on YouTube.
        max_videos (int): The maximum number of videos to index. Default is 10.
        max_duration (int): The maximum duration of videos to index in seconds. Default is 600.

        Returns:
        dict: JSON containing indexed videos.
        """
        url = f"{self.api_url}/index/{index_name}/youtube/search"
        body = {"search_term": search_term, "max_videos": max_videos, "max_duration": max_duration}
        response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_from_youtube_url(self, 
                              index_name: str, 
                              url: str, 
                              max_videos: int = 10, 
                              max_duration: int = 600) -> Dict:
        """
        Index videos from a specific YouTube URL.

        Parameters:
        index_name (str): The name of the index to add the videos to.
        url (str): The URL of the YouTube video.
        max_videos (int): The maximum number of videos to index. Default is 10.
        max_duration (int): The maximum duration of videos to index in seconds. Default is 600.

        Returns:
        dict: JSON containing indexed videos.
        """
        api_url = f"{self.api_url}/index/{index_name}/youtube/url"
        body = {"url": url, "max_videos": max_videos, "max_duration": max_duration}
        response = requests.post(api_url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_from_youtube_playlist(self, 
                                   index_name: str, 
                                   playlist_url: str, 
                                   max_videos: int = 10, 
                                   max_duration: int = 600) -> Dict:
        """
        Index videos from a YouTube playlist.

        Parameters:
        index_name (str): The name of the index to add the videos to.
        playlist_url (str): The URL of the YouTube playlist.
        max_videos (int): The maximum number of videos to index. Default is 10.
        max_duration (int): The maximum duration of videos to index in seconds. Default is 600.

        Returns:
        dict: JSON containing indexed videos.
        """
        api_url = f"{self.api_url}/index/{index_name}/youtube/playlist"
        body = {"playlist_url": playlist_url, "max_videos": max_videos, "max_duration": max_duration}
        response = requests.post(api_url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_from_youtube_channel(self, 
                                  index_name: str, 
                                  channel_url: str, 
                                  max_videos: int = 10, 
                                  max_duration: int = 600) -> Dict:
        """
        Index videos from a YouTube channel.

        Parameters:
        index_name (str): The name of the index to add the videos to.
        channel_url (str): The URL of the YouTube channel.
        max_videos (int): The maximum number of videos to index. Default is 10.
        max_duration (int): The maximum duration of videos to index in seconds. Default is 600.

        Returns:
        dict: JSON containing indexed videos.
        """
        api_url = f"{self.api_url}/index/{index_name}/youtube/channel"
        body = {"channel_url": channel_url, "max_videos": max_videos, "max_duration": max_duration}
        response = requests.post(api_url, json=body, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def index_video(self, 
                   index_name: str, 
                   video_path: Optional[str] = None, 
                   video_url: Optional[str] = None, 
                   transcript_path: Optional[str] = None, 
                   metadata: Dict = {}) -> Dict:
        """
        Index a local video file along with optional transcript and metadata.

        Parameters:
        index_name (str): The name of the index to add the video to.
        video_path (str, optional): The local file path to the video. Default is None.
        video_url (str, optional): The URL of the video. Default is None.
        transcript_path (str, optional): The local file path to the transcript. Default is None.
        metadata (dict): Additional metadata for the video.

        Returns:
        dict: JSON with the video details of the indexed video.

        Raises:
        ValueError: If neither video_path nor video_url is provided.
        """
        url = f"{self.api_url}/index/{index_name}/video"
        files = {}
        params = {}
        if video_path:
            files["video_file"] = open(video_path, "rb")
        elif video_url:
            params["video_url"] = video_url
        else:
            raise ValueError("Either video_path or video_url must be provided.")

        if transcript_path:
            files["transcript"] = open(transcript_path, "rb")

        # Move all non-member metadata to info dictionary.
        info = {}
        for k in list(metadata.keys()):
            if k not in ['url', 'transcript', 'title', 'description']:
                info[k] = metadata.pop(k)
        metadata['info'] = info

        metadata_str = json.dumps(metadata)
        body = {'metadata_str': metadata_str}
        response = requests.post(url, files=files, data=body, params=params, headers=self.headers, stream=True)
        
        # Close file handles
        for file_obj in files.values():
            file_obj.close()
            
        response.raise_for_status()
        return response.json()

    def index_image(self, 
                   index_name: str, 
                   image_path: Optional[str] = None, 
                   image_url: Optional[str] = None, 
                   metadata: Dict = {}) -> Dict:
        """
        Index an image from a local file or a URL with optional metadata.

        Parameters:
        index_name (str): The name of the index to add the image to.
        image_path (str, optional): The local file path to the image. Default is None.
        image_url (str, optional): The URL of the image. Default is None.
        metadata (dict, optional): Additional metadata for the image. Default is an empty dictionary.

        Returns:
        dict: JSON response with the details of the indexed image.

        Raises:
        ValueError: If neither image_path nor image_url is provided.
        """
        url = f"{self.api_url}/index/{index_name}/image"
        files = {}
        params = {}
        if image_path:
            files["image_file"] = open(image_path, "rb")
        elif image_url:
            params["image_url"] = image_url
        else:
            raise ValueError("Either image_path or image_url must be provided.")
        metadata_str = json.dumps(metadata)
        body = {"metadata_str": metadata_str}
        response = requests.post(url, files=files, data=body, params=params, headers=self.headers)
        
        # Close file handles
        for file_obj in files.values():
            file_obj.close()
            
        response.raise_for_status()
        return response.json()

    def get_video_metadata(self, index_name: str, video_id: str) -> Dict:
        """
        Retrieve video metadata corresponding to video_id.

        Parameters:
        index_name (str): The name of the index containing the video.
        video_id (str): The id of the video.

        Returns:
        dict: JSON with the video metadata.
        """
        url = f"{self.api_url}/index/{index_name}/video/{video_id}/metadata"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_video_metadata(self, index_name: str, video_id: str, metadata: Dict) -> Dict:
        """
        Update video metadata corresponding to video_id.

        Parameters:
        index_name (str): The name of the index containing the video.
        video_id (str): The id of the video.
        metadata (dict): Updated metadata to overwrite.

        Returns:
        dict: JSON with the updated video metadata.
        """
        url = f"{self.api_url}/index/{index_name}/video/{video_id}/metadata"
        response = requests.put(url, json=metadata, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    def update_video_transcript(self, index_name: str, video_id: str, transcript_path: str) -> Dict:
        """
        Update transcript for a specific video.
        
        Parameters:
        index_name (str): The name of the index.
        video_id (str): The ID of the video.
        transcript_path (str): Path to the transcript file.
        
        Returns:
        dict: JSON response with the updated video information.
        """
        url = f"{self.api_url}/index/{index_name}/video/{video_id}/transcript"
        with open(transcript_path, "rb") as transcript_file:
            files = {"transcript": transcript_file}
            response = requests.post(url, files=files, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    def get_video_attention_map(self, index_name: str, video_id: str) -> Dict:
        """
        Get the attention map for a specific video.
        
        Parameters:
        index_name (str): The name of the index.
        video_id (str): The ID of the video.
        
        Returns:
        dict: JSON containing the attention map.
        """
        url = f"{self.api_url}/index/{index_name}/video/{video_id}/attention"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_assets(self, index_name: str) -> Dict:
        """
        List all assets (videos and images) in the specified index.

        Parameters:
        index_name (str): The name of the index.

        Returns:
        dict: JSON that lists all assets in index.
        """
        url = f"{self.api_url}/index/{index_name}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_videos(self, index_name: str) -> Dict:
        """
        List all videos in the specified index.

        Parameters:
        index_name (str): The name of the index.

        Returns:
        dict: JSON that lists all videos in index.
        """
        url = f"{self.api_url}/index/{index_name}/videos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    def get_video(self, index_name: str, video_id: str) -> Dict:
        """
        Get details for a specific video.
        
        Parameters:
        index_name (str): The name of the index.
        video_id (str): The ID of the video.
        
        Returns:
        dict: JSON containing the video details.
        """
        url = f"{self.api_url}/index/{index_name}/video/{video_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    def get_stats(self) -> Dict:
        """
        Get usage statistics for the current user.
        
        Returns:
        dict: JSON containing statistics including number of videos, total runtime, and disk usage.
        """
        url = f"{self.api_url}/stats"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    def cluster(self, 
               index_name: str,
               visualization_mode: str = "tsne",
               clustering_algorithm: str = "kmeans",
               canonical_query_path: Optional[str] = None,
               start_seconds: int = 0,
               end_seconds: int = -1,
               asset_ids: Optional[List[str]] = None,
               projection_mode: Optional[str] = None) -> Dict:
        """
        Create a cluster visualization of videos and images in the index.
        
        Parameters:
        index_name (str): The name of the index.
        visualization_mode (str): The visualization algorithm to use. Default is "tsne".
        clustering_algorithm (str): The clustering algorithm to use. Default is "kmeans".
        canonical_query_path (str, optional): Path to an image or video file to use as canonical query.
        start_seconds (int): Start time for video canonical query in seconds. Default is 0.
        end_seconds (int): End time for video canonical query in seconds. Default is -1 (end of video).
        asset_ids (list, optional): List of asset IDs to include in the clustering.
        projection_mode (str, optional): Projection mode for dimensionality reduction.
        
        Returns:
        dict: JSON containing the clustering results and visualization data.
        """
        url = f"{self.api_url}/index/{index_name}/cluster"
        files = {}
        data = {
            "visualization_mode": visualization_mode,
            "clustering_algorithm": clustering_algorithm,
            "start_seconds": start_seconds,
            "end_seconds": end_seconds,
        }
        
        if canonical_query_path:
            with open(canonical_query_path, "rb") as f:
                is_video = canonical_query_path.lower().endswith(('.mp4', '.mov', '.avi', '.wmv'))
                content_type = "video/mp4" if is_video else "image/jpeg"
                files["canonical_query"] = (os.path.basename(canonical_query_path), f, content_type)
                
        if asset_ids:
            data["asset_ids"] = ",".join(asset_ids)
            
        if projection_mode:
            data["projection_mode"] = projection_mode if projection_mode != "none" else "none"
        
        response = requests.post(url, files=files, data=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
if __name__ == '__main__':
    api_key = "your_api_key"
    api_url = "https://api.askvideos.com"  # or your custom API URL

    client = Client(api_key, api_url)

    # Example usage:
    
    # Create an index
    index_name = "my_video_index"
    client.create_index(index_name)

    # Index a video from URL
    video_result = client.index_video(
        index_name,
        video_url='https://example.com/sample.mp4',
        metadata={
            "title": "Sample Video",
            "description": "A sample video for testing",
            "tags": ["sample", "test"]
        }
    )
    
    # Search for videos with a query
    search_results = client.search_videos(
        index_name, 
        "people walking on beach", 
        modes=["video"], 
        top_k=5
    )
    
    # Get an answer from the indexed videos
    answer = client.answer(
        index_name,
        "What activities are shown in the videos?",
        use_markdown=True
    )
    
    print(f"Answer: {answer['answer']}")
