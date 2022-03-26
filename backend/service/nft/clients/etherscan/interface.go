package etherscan

import (
	"context"

	"github.com/dapp-z/auction/backend/service/nft/models"
)

type Client interface {
	GetNFTsByWalletAddress(ctx context.Context, address string) ([]models.NFT, error)
}
