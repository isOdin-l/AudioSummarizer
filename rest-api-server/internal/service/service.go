package service

type IRepository interface {
	IAudioRepository
	IUserRepository
}

type Service struct {
	AudioService
	UserService
}

func NewService(repo IRepository) *Service {
	return &Service{
		AudioService: *NewAudioService(repo),
		UserService:  *NewUserService(repo),
	}
}
