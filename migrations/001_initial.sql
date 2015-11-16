-- emoticon
CREATE TABLE IF NOT EXISTS emoticon (
    id SERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE emoticon IS 'Stores ascii emoticons identified by a base name.';
COMMENT ON COLUMN emoticon.id IS 'primary key';
COMMENT ON COLUMN emoticon.name IS 'emoticon main alias';
COMMENT ON COLUMN emoticon.content IS 'emoticon text content';
COMMENT ON COLUMN emoticon.created_at IS 'when an emoticon was added';


-- emoticon_alias
CREATE TABLE IF NOT EXISTS emoticon_alias (
    id SERIAL NOT NULL PRIMARY KEY,
    emoticon_id INT NOT NULL,
    name VARCHAR(20) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (emoticon_id) REFERENCES emoticon (id) ON DELETE CASCADE
);

COMMENT ON TABLE emoticon_alias IS 'Stores ascii emoticons identified by a base name.';
COMMENT ON COLUMN emoticon_alias.id IS 'primary key';
COMMENT ON COLUMN emoticon_alias.emoticon_id IS 'foreign key to emoticon table';
COMMENT ON COLUMN emoticon_alias.name IS 'emoticon alternate alias';
COMMENT ON COLUMN emoticon.created_at IS 'when an emoticon alias was added to an emoticon';
