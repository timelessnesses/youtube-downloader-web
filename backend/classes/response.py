import enum
import typing

import pydantic
import yarl
import datetime

class Status(enum.Enum):
    success = "success"
    error = "error"


class BaseResponse(pydantic.BaseModel):
    status: Status
    error: typing.Optional[str]


class Stream(pydantic.BaseModel):
    abr: typing.Optional[str]
    audio_codec: typing.Optional[str]
    bitrate: typing.Optional[int]
    size: int
    progressive: bool
    adaptive: bool
    fps: int = 0  # audio
    hdr: bool
    resolution: typing.Optional[str]
    mimetype: str
    codec: typing.Any


class StreamsResponse(BaseResponse):
    streams: typing.Any


class Caption(pydantic.BaseModel):
    code: str
    name: str
    url: str

class Video(pydantic.BaseModel):
    title: str
    age_restricted: bool
    author: str
    length: int
    thumbnail: str
    streams: list[Stream]
class CaptionsResponse(BaseResponse):
    captions: list[Caption]
    
class PlaylistStreamsResponse(BaseResponse):
    videos: list[Video]
    name: str
    video_counts: int
    description: str
    last_update: typing.Union[str, datetime.datetime]
    owner: str
    owner_url: typing.Union[str, yarl.URL]
    views: int
    
    
class DownloadResponse(BaseResponse):
    at: pydantic.HttpUrl
    size: int
