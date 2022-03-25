package app

import (
	"go.uber.org/fx"

	"github.com/dapp-z/auction/backend/pkg/config"
	"github.com/dapp-z/auction/backend/pkg/http"
)

var BaseModule = fx.Options(
	config.Module,
	http.Module,
)
