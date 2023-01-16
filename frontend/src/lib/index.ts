import Axios from 'axios';
import type { AxiosResponse } from 'axios';
import { backend_url } from 'src/config';
import type { SearchResult, VideoStream, Caption, Playlist } from 'src/lib/interface';
import {
	convert_to_search_result,
	convert_to_video_stream,
	convert_to_captions,
	convert_to_playlist
} from 'src/lib/converters';
// could create callback on 400 and 500 errors
const axios = Axios.create({
	baseURL: backend_url
});

async function get(url: string): Promise<AxiosResponse> {
	const res = await axios.get(url);
	if (res.status === 200) {
		// :D
		return res;
	} else {
		throw new Error(`Error: ${res.status}`);
	}
}

export async function get_search_results(search_term: string): Promise<SearchResult> {
	const response = await get(`/search/${search_term}`);
	return convert_to_search_result(response.data);
}

export async function get_search_auto_complete(search_term: string): Promise<SearchResult> {
	const response = await get(`/search/autocomplete/${search_term}`);
	return convert_to_search_result(response.data);
}

export async function get_video_streams(video_id: string): Promise<VideoStream[]> {
	const response = await get(`/video/streams/${video_id}`);
	return convert_to_video_stream(response.data);
}

export async function get_video_captions(video_id: string): Promise<Caption[]> {
	const response = await get(`/video/captions/${video_id}`);
	return convert_to_captions(response.data);
}

export async function get_playlist_videos(playlist_id: string): Promise<Playlist> {
	const response = await get(`/playlist/videos/${playlist_id}`);
	return convert_to_playlist(response.data);
}
