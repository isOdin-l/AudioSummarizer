package config

import (
	"fmt"

	"github.com/caarlos0/env/v11"
)

type S3Config struct {
	Endpoint  string `env:"S3_ENDPOINT"`
	Port      string `env:"S3_PORT"`
	AccessKey string `env:"S3_ACCESS_KEY"`
	SecretKey string `env:"S3_SECRET_KEY"`
	Bucket    string `env:"S3_BUCKET"`
	Region    string `env:"S3_REGION"`
}

func (cfg *S3Config) DSN() string {
	return fmt.Sprintf("%s:%s", cfg.Endpoint, cfg.Port)

}

type PostgresConfig struct {
	Host     string `env:"POSTGRES_HOST"`
	Port     string `env:"POSTGRES_PORT"`
	Name     string `env:"POSTGRES_DB"`
	Username string `env:"POSTGRES_USER"`
	Password string `env:"POSTGRES_PASSWORD"`
}

func (cfg *PostgresConfig) DSN() string {
	return fmt.Sprintf("postgres://%s:%s@%s:%s/%s", cfg.Username, cfg.Password, cfg.Host, cfg.Port, cfg.Name)
}

type KafkaConfig struct {
	BootstrapSevers []string `env:"KAFKA_BOOTSTRAP_SERVERS"`
	GroupId         string   `env:"KAFKA_GROUP_ID"`
	Topic           string   `env:"KAFKA_TOPIC"`
}

type ServerConfig struct {
	Port string `env:"SERVER_PORT"`
}

type JWTConfig struct {
	Salt string `env:"SALT"`
}

// TODO: подумать - мб переделать этот бред
type Config struct {
	S3Config       S3Config
	PostgresConfig PostgresConfig
	KafkaConfig    KafkaConfig
	ServerConfig   ServerConfig
	JWTConfig      JWTConfig
}

func InitConfig() (*Config, error) {
	s3, err := env.ParseAs[S3Config]()
	if err != nil {
		return nil, err
	}

	db, err := env.ParseAs[PostgresConfig]()
	if err != nil {
		return nil, err
	}

	kafka, err := env.ParseAs[KafkaConfig]()
	if err != nil {
		return nil, err
	}

	server, err := env.ParseAs[ServerConfig]()
	if err != nil {
		return nil, err
	}

	jwt, err := env.ParseAs[JWTConfig]()
	if err != nil {
		return nil, err
	}

	return &Config{
		S3Config:       s3,
		PostgresConfig: db,
		KafkaConfig:    kafka,
		ServerConfig:   server,
		JWTConfig:      jwt,
	}, nil
}
