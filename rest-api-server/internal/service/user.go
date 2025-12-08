package service

type IUserRepository interface {
	CreateUser()
	GetUser()
}

type UserService struct {
	repo IUserRepository
}

func NewUserService(repo IUserRepository) *UserService {
	return &UserService{
		repo: repo,
	}
}

func (s *UserService) SignUp() {

}

func (s *UserService) SignIn() {

}
