package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/isOdin-l/AudioSummarizer/internal/config"
	"github.com/isOdin-l/AudioSummarizer/internal/database"
	"github.com/isOdin-l/AudioSummarizer/internal/handler"
	"github.com/isOdin-l/AudioSummarizer/internal/repository"
	"github.com/isOdin-l/AudioSummarizer/internal/router"
	"github.com/isOdin-l/AudioSummarizer/internal/server"
	"github.com/isOdin-l/AudioSummarizer/internal/service"
	"github.com/labstack/gommon/log"
)

func main() {
	// Контекст для graceful shutdown
	gcCtx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	// Инициализация Конфига
	cfg, err := config.InitConfig()
	if err != nil {
		log.Error("Error while initializing config: ", err.Error())
		return
	}

	// DB
	db, err := database.NewPostgresDB(&cfg.PostgresConfig)
	if err != nil {
		log.Error("Error while initilizing database: ", err.Error())
		return
	}
	defer db.Close()

	// S3
	s3Storage, err := database.NewMinioDB(&cfg.S3Config)
	if err != nil {
		log.Error("Error while initilizing s3 storage: ", err.Error())
		return
	}

	// Kafka
	kafka := database.NewKafka(&cfg.KafkaConfig)
	defer kafka.Close()

	// Repository
	repository := repository.NewRepository(db, s3Storage, kafka)

	// Service
	service := service.NewService(repository)

	// Handler
	handler := handler.NewHandler(service)

	// Routing
	router := router.NewRouter(handler)

	// Server
	server := server.NewServer(router, &cfg.ServerConfig)

	// Starting
	go func() {
		if err := server.ListenAndServeTLS("", ""); err != nil && err != http.ErrServerClosed {
			log.Fatal(err)
		}
	}()

	// Graceful Shutdown
	<-gcCtx.Done()

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := server.Shutdown(ctx); err != nil {
		log.Fatal(err)
	}
}
