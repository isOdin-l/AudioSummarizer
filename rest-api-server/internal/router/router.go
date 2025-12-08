package router

import (
	"github.com/labstack/echo/v4"
)

type IHandler interface {
	SignUp(c echo.Context) error
	SignIn(c echo.Context) error

	Summirise(c echo.Context) error
}

func NewRouter(h IHandler) *echo.Echo {
	e := echo.New()
	api := e.Group("/api/v0")

	api.POST("/sign_up", h.SignUp)
	api.POST("/sign_in", h.SignIn)
	api.POST("/summirise", h.Summirise)

	return e
}
