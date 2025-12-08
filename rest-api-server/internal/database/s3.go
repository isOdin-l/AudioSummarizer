package database

import (
	"github.com/isOdin-l/AudioSummarizer/internal/config"
	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

func NewMinioDB(cfg *config.S3Config) (*minio.Client, error) {
	minioStorage, err := minio.New(cfg.DSN(), &minio.Options{
		Region: cfg.Region,
		Creds:  credentials.NewStaticV4(cfg.AccessKey, cfg.SecretKey, ""),
	})

	if err != nil {
		return nil, err
	}

	return minioStorage, nil
}
