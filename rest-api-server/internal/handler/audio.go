package handler

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

type IAudioService interface {
	Upload()
	Download()
}

type AudioHandler struct {
	service IAudioService
}

func NewAudioHandler(service IAudioService) *AudioHandler {
	return &AudioHandler{
		service: service,
	}
}

func (h *AudioHandler) Summirise(c echo.Context) error {
	return c.NoContent(http.StatusOK)
}
