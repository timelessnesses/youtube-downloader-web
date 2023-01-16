// @ts-nocheck

import type { SearchResult, VideoStream } from 'src/lib/interface'
import type { AxiosResponse } from 'axios'

export function convert_to_search_result(response: AxiosResponse): SearchResult {
    return {
        results: response.results as Array<string> // can you not typescript
    }
}

export function convert_to_video_stream(response: AxiosResponse): VideoStream[] {
    return response.streams.map((stream: object) => {
        return {
            abr: stream.abr as number | null,
            audio_codec: stream.audio_codec as string | null,
            bitrate: stream.bitrate as number | null,
            size: stream.size as number | null,
            progressive: stream.progressive as boolean,
            adaptive: stream.adaptive as boolean,
            fps: stream.fps as number | null,
            hdr: stream.hdr as boolean,
            resolution: stream.resolution as string | null,
            mimetype: stream.mimetype as string,
            codec: stream.codec as string
        }
    })
}

export function convert_to_captions(response: AxiosResponse): Caption[] {
    return response.captions.map((caption: object) => {
        return {
            code: caption.code as string,
            name: caption.name as string,
            url: caption.url as string
        }
    })
}

export function convert_to_playlist(response: AxiosResponse): Playlist {
    return {
        videos: convert_to_video_stream(response.videos),
        name: response.name as string,
        video_count: response.video_count as number,
        description: response.description as string,
        last_updated: response.last_updated as string,
        owner: response.owner as string,
        owner_url: response.owner_url as string,
        views: response.views as number
    }
}