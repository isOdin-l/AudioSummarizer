package server

import (
	"crypto/tls"
	"net/http"

	"golang.org/x/crypto/acme"

	"github.com/isOdin-l/AudioSummarizer/internal/config"
	"github.com/labstack/echo/v4"
	"golang.org/x/crypto/acme/autocert"
)

func NewServer(router *echo.Echo, cfg *config.ServerConfig) *http.Server {

	autoTLSManager := autocert.Manager{
		Prompt: autocert.AcceptTOS,
		// Cache certificates to avoid issues with rate limits (https://letsencrypt.org/docs/rate-limits)
		Cache: autocert.DirCache("/var/www/.cache"),
		//HostPolicy: autocert.HostWhitelist("<DOMAIN>"),
	}
	s := &http.Server{
		Addr:    cfg.Port,
		Handler: router,
		TLSConfig: &tls.Config{
			//Certificates: nil, // <-- s.ListenAndServeTLS will populate this field
			GetCertificate: autoTLSManager.GetCertificate,
			NextProtos:     []string{acme.ALPNProto},
		},
	}

	return s
}
