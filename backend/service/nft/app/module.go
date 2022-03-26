package app

import (
	"go.uber.org/fx"

	"github.com/dapp-z/auction/backend/pkg/app"
	"github.com/dapp-z/auction/backend/service/nft/clients/etherscan"
	"github.com/dapp-z/auction/backend/service/nft/http"
)

var BaseModule = fx.Options(
	app.BaseModule,
	etherscan.Module,
	http.Module,
)
