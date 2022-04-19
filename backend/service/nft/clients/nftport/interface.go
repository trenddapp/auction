package nftport

import (
	"context"

	"github.com/dapp-z/auction/backend/service/nft/models"
)

type Client interface {
	GetAccountNFTs(ctx context.Context, address string) ([]models.NFT, error)
	GetContractNFTs(ctx context.Context, address string) ([]models.NFT, error)
	GetNFT(ctx context.Context, contractAddress string, tokenID string) (*models.NFT, error)
}
