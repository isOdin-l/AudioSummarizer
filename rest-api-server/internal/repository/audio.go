package repository

import (
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/minio/minio-go/v7"
	"github.com/segmentio/kafka-go"
)

type AudioRepository struct {
	db             pgxpool.Pool
	s3             minio.Client
	messageBrocker kafka.Writer
}

func NewAudioRepository(db *pgxpool.Pool, s3 *minio.Client, messageBrocker *kafka.Writer) *AudioRepository {
	return &AudioRepository{
		db:             *db,
		s3:             *s3,
		messageBrocker: *messageBrocker,
	}
}

func (r *AudioRepository) CreateAudioDb() {

}

func (r *AudioRepository) UploadAudioS3() {

}

func (r *AudioRepository) DownloadSummaryS3() {

}

func (r *AudioRepository) AddDataToMsgBroker() {

}
