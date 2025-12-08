package database

import (
	"context"

	"github.com/isOdin-l/AudioSummarizer/internal/config"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/labstack/gommon/log"
)

func NewPostgresDB(cfg *config.PostgresConfig) (*pgxpool.Pool, error) {
	conn, err := pgxpool.New(context.Background(), cfg.DSN())
	if err != nil {
		return nil, err
	}

	if err := conn.Ping(context.Background()); err != nil {
		return nil, err
	}

	log.Info("Database connected")
	return conn, nil
}
