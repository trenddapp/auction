package http

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/dapp-z/auction/backend/service/nft/clients/etherscan"
)

type Server struct {
	clientEtherscan etherscan.Client
}

func NewServer(clientEtherscan etherscan.Client) *Server {
	return &Server{
		clientEtherscan: clientEtherscan,
	}
}

func (s *Server) GetNFTs(c *gin.Context) {
	address := c.Query("address")
	if address == "" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "invalid address",
		})

		return
	}

	nfts, err := s.clientEtherscan.GetNFTsByWalletAddress(c, address)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":   "internal server error",
			"message": err.Error(),
		})

		return
	}

	c.JSON(http.StatusOK, gin.H{
		"nfts": nfts,
	})
}
