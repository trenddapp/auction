package app

import (
	"go.uber.org/fx"

	"github.com/dapp-z/auction/backend/pkg/app"
	clientetherscan "github.com/dapp-z/auction/backend/service/nft/clients/etherscan"
	clientnftport "github.com/dapp-z/auction/backend/service/nft/clients/nftport"
	"github.com/dapp-z/auction/backend/service/nft/http"
)

var BaseModule = fx.Options(
	app.BaseModule,
	clientetherscan.Module,
	clientnftport.Module,
	http.Module,
)
