package repository

import (
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/minio/minio-go/v7"
	"github.com/segmentio/kafka-go"
)

type Repository struct {
	UserRepository
	AudioRepository
}

func NewRepository(db *pgxpool.Pool, s3 *minio.Client, messageBrocker *kafka.Writer) *Repository {
	return &Repository{
		UserRepository:  *NewUserRepository(db),
		AudioRepository: *NewAudioRepository(db, s3, messageBrocker),
	}
}
