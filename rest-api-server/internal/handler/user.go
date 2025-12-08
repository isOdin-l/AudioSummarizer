package handler

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

type IUserService interface {
	SignUp()
	SignIn()
}

type UserHandler struct {
	service IUserService
}

func NewUserHandler(service IUserService) *UserHandler {
	return &UserHandler{
		service: service,
	}
}

func (h *UserHandler) SignUp(c echo.Context) error {
	return c.NoContent(http.StatusOK)
}

func (h *UserHandler) SignIn(c echo.Context) error {
	return c.NoContent(http.StatusOK)
}
