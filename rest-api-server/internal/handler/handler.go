package handler

type IService interface {
	IAudioService
	IUserService
}

type Handler struct {
	AudioHandler
	UserHandler
}

func NewHandler(service IService) *Handler {
	return &Handler{
		AudioHandler: *NewAudioHandler(service),
		UserHandler:  *NewUserHandler(service),
	}
}
