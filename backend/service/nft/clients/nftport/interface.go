package nftport

import (
	"context"

	"github.com/dapp-z/auction/backend/service/nft/models"
)

type Client interface {
	GetContractNFTs(ctx context.Context, address string) ([]models.NFT, error)
}
