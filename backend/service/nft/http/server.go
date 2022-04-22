package http

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/dapp-z/auction/backend/service/nft/clients/etherscan"
	"github.com/dapp-z/auction/backend/service/nft/clients/nftport"
)

type Server struct {
	clientEtherscan etherscan.Client
	clientNFTPort   nftport.Client
}

func NewServer(clientEtherscan etherscan.Client, clientNFTPort nftport.Client) *Server {
	return &Server{
		clientEtherscan: clientEtherscan,
		clientNFTPort:   clientNFTPort,
	}
}

func (s *Server) GetAccountNFTs(ctx *gin.Context) {
	address := ctx.Param("address")
	if address == "" {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"error": "invalid address",
		})

		return
	}

	nfts, err := s.clientEtherscan.GetAccountNFTs(ctx, address)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"error": err.Error(),
		})

		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"nfts": nfts,
	})
}

func (s *Server) GetContractNFTs(ctx *gin.Context) {
	address := ctx.Param("address")
	if address == "" {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"error": "invalid address",
		})

		return
	}

	nfts, err := s.clientNFTPort.GetContractNFTs(ctx, address)
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"error": err.Error(),
		})

		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"nfts": nfts,
	})
}
