CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE multiplatform_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(128) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE singleplatform_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES multiplatform_accounts(id) ON DELETE SET NULL,
    interaction_data TEXT NOT NULL UNIQUE,
    type VARCHAR(32) NOT NULL,
    meta_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX sp_accounts_user_id_idx ON singleplatform_accounts(user_id);
CREATE INDEX sp_accounts_interaction_data_idx ON singleplatform_accounts(interaction_data);

CREATE TABLE audio_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES multiplatform_accounts(id) ON DELETE CASCADE DEFAULT NULL,
    source_id UUID REFERENCES singleplatform_accounts(id) ON DELETE CASCADE NOT NULL,
    s3_filename TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX audio_files_user_id_idx ON audio_files(user_id);
CREATE INDEX audio_files_source_id_idx ON audio_files(source_id);

CREATE TABLE transcriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audio_id UUID REFERENCES audio_files(id) ON DELETE CASCADE NOT NULL,
    s3_filename TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX transcriptions_audio_id_idx ON transcriptions(audio_id);


CREATE TABLE summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audio_id UUID REFERENCES audio_files(id) ON DELETE CASCADE NOT NULL,
    s3_filename TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX summaries_audio_id_idx ON summaries(audio_id);
