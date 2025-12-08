package database

import (
	"github.com/isOdin-l/AudioSummarizer/internal/config"
	"github.com/segmentio/kafka-go"
)

func NewKafka(cfg *config.KafkaConfig) *kafka.Writer {
	return kafka.NewWriter(kafka.WriterConfig{
		Brokers: cfg.BootstrapSevers,
		Topic:   cfg.Topic,
	})
}
