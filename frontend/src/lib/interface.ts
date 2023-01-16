export interface SearchResult {
	results: Array<string>;
}

export interface VideoStream {
	abr: number | null;
	audio_codec: string | null;
	bitrate: number | null; // videos only
	size: number | null;
	progressive: boolean;
	adaptive: boolean;
	fps: number | null; // could default this to 0
	hdr: boolean;
	resolution: string | null;
	mimetype: string;
	codec: [Array<string>, Array<string>];
}

export interface Caption {
	code: string;
	name: string;
	url: string;
}

export interface Video {
	title: string;
	age_restricted: boolean;
	author: string;
	length: number;
	thumbnail: string;
	id: string;
	streams: Array<VideoStream>;
}

export interface Playlist {
	videos: Array<Video>;
	name: string;
	video_count: number;
	description: string;
	last_updated: string;
	owner: string;
	owner_url: string;
	views: number;
}
