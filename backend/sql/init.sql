CREATE TABLE IF NOT EXISTS cache (
    id TEXT, /* video id */
    data BYTEA NOT NULL, /* video data */
    when_ TIMESTAMP NOT NULL, /* when the video was cached  so we can do check */
    cache_id TEXT PRIMARY KEY /* cache id */
)