import asyncpg
from dotenv import load_dotenv
from fastapi import FastAPI, Request, BackgroundTasks
from pytube import Caption, Playlist, Search, YouTube, StreamQuery

load_dotenv()
import logging
import os
import io
import asyncio
import zipfile

import yarl
import pydantic
import typing
from datetime import datetime
from backend.classes import response
from backend.utils.id_gen import generate_id

app = FastAPI(title="Youtube Downloader Backend", docs_url="/")
app.db: asyncpg.pool.Pool = None
app.log = logging.getLogger("YoutubeDownloaderBackend")


@app.get("/video/streams/{video_id}", response_model=response.StreamsResponse)
async def youtube(video_id: typing.Union[str, pydantic.HttpUrl]):
    yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
    
    j = {
        "status": "success",
        "streams": [
            {
                "abr": stream.abr,
                "audio_codec": stream.audio_codec,
                "bitrate": stream.bitrate,
                "size": stream.filesize_approx,
                "progressive": stream.is_progressive,
                "adaptive": stream.is_adaptive,
                "fps": stream.__dict__.get("fps", 0),
                "hdr": stream.is_hdr,
                "resolution": stream.resolution,
                "mimetype": stream.mime_type,
                "codec": stream.parse_codecs(),
            }
            for stream in yt.streams.asc()
        ],
    }
    return j


@app.get("/video/captions/{video_id}", response_model=response.CaptionsResponse)
async def captions(video_id: str):
    yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
    j = {
        "status": "success",
        "captions": [
            {"code": caption.code, "name": caption.name, "url": caption.url}
            for caption in yt.captions.all()
        ],
    }
    print(j)
    return j


@app.get(
    "/playlist/streams/{playlist_id}", response_model=response.PlaylistStreamsResponse
)
async def playlist(playlist_id: str):
    pl = Playlist("https://www.youtube.com/playlist?list=" + playlist_id)
    stream: StreamQuery
    j = {
        "status": "success",
        "videos": [
            {
                "title": video.title,
                "age_restricted": video.age_restricted,
                "author": video.author,
                "length": video.length,
                "thumbnail": video.thumbnail_url,
                "id": video.video_id,
                "streams": [
                    {
                        "abr": stream.abr,
                        "audio_codec": stream.audio_codec,
                        "bitrate": stream.bitrate,
                        "size": stream.filesize_approx,
                        "progressive": stream.is_progressive,
                        "adaptive": stream.is_adaptive,
                        "fps": stream.__dict__.get("fps", 0),
                        "hdr": stream.is_hdr,
                        "resolution": stream.resolution,
                        "mimetype": stream.mime_type,
                        "codec": stream.parse_codecs(),
                        "itag": stream.itag,
                    }
                    for stream in video.streams.asc()
                ],
            }
            for video in pl.videos
        ],
        "name": pl.title,
        "video_counts": pl.count,
        "description": pl.description,
        "last_updated": pl.last_updated,
        "owner": pl.owner,
        "owner_url": pl.owner_url,
        "views": pl.views,
        "id": pl.playlist_id,
    }
    return j

@app.post("/video/download/{id}/{itag}")
async def download(id: str, itag: str, request: Request):
    try:
        yt = YouTube("https://www.youtube.com/watch?v=" + id)
        stream = yt.streams.get_by_itag(itag)
        j = io.BytesIO()
        stream.stream_to_buffer(j)
        await app.db.execute(
            """
            INSERT INTO cache (id, data, cache_id, when_) VALUES ($1, $2, $3, $4)
            """,
            id,
            j.read(),
            generate_id(1000),
            datetime.now()
        )
    except Exception as e:
        return {
            "status": "error",
            "error": "{} {}".format(type(e).__name__, e)
        }
    return {
        "status": "success",
        "at": str(yarl.URL(request.url).with_path("/video/download/{}".format(id))),
        "size": stream.filesize_approx
    }

@app.post("/playlist/download/{id}/{itag}")   
async def bulk_download_playlist(id: str, itag: str, request: Request):
    playlist = Playlist("https://www.youtube.com/playlist?list=" + id)
    files = {}
    for video in playlist.videos:
        stream = video.streams.get_by_itag(itag)
        j = io.BytesIO()
        stream.stream_to_buffer(j)
        files[stream.default_filename] = j
    b = io.BytesIO()
    zipping = zipfile.ZipFile(b, "w")
    for filename, data in files.items():
        zipping.writestr(filename, data.getvalue())
    zipping.comment("Thanks for using Youtube Downloader Backend!".encode("utf-8"))
    zipping.close()
    await app.db.execute(
        """
        INSERT INTO cache (id, data, cache_id, when_) VALUES ($1, $2, $3, $4)
        """,
        id,
        b.getvalue(),
        generate_id(1000),
        datetime.now()
    )

@app.get("/search/autocomplete/{query}")
async def autocomplete(query: str):
    return {
        "status": "success",
        "results": [
            x for x in Search(query).completion_suggestions
        ]
    }

@app.get("/search/{query}")
async def search(query: str):
    videos: typing.List[YouTube] = Search(query).fetch_and_parse()[0]
    return {
        "status": "success",
        "results": [
            {
                "author": video.author,
                "title": video.title,
                "length": video.length,
                "thumbnail": video.thumbnail_url,
                "id": video.video_id
            }
            for video in videos
        ]
    }

@app.get("/database/size")
async def db_size():
    return {
        "status": "success",
        "size": await app.db.fetchval("SELECT pg_database_size(cache)")
    }

@app.get("/database/count")
async def db_element_count():
    return {
        "status": "success",
        "videos": await app.db.fetchval("SELECT COUNT(*) FROM cache")
    }

@app.on_event("startup")
async def startup_event():
    app.db = await asyncpg.create_pool(
        f"postgresql://{os.getenv('POSTGRESQL_USER')}:{os.getenv('POSTGRESQL_PASSWORD')}@{os.getenv('POSTGRESQL_HOST')}:{os.getenv('POSTGRESQL_PORT')}/{os.getenv('POSTGRESQL_DATABASE')}"
    )
    with open("backend/sql/init.sql") as fp:
        j = fp.read()
    await app.db.execute(j)
    asyncio.create_task(delete_video_occasionally())

async def delete_video_occasionally():
    while True:
        await app.db.execute(
            """
            DELETE FROM cache WHERE when_ < NOW() - INTERVAL '7 day'
            """
        )
        await asyncio.sleep(1200)
        