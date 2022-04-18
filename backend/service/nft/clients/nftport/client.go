package nftport

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"net/http"

	"github.com/dapp-z/auction/backend/service/nft/models"
)

const (
	StatusOK = "OK"
	URL      = "https://api.nftport.xyz"
)

var (
	ErrUnknown = errors.New("unknown error")
)

type client struct {
	apiKey     string
	httpClient *http.Client
}

func NewClient(config *Config) Client {
	return &client{
		apiKey:     config.APIKey,
		httpClient: http.DefaultClient,
	}
}

func (c *client) GetContractNFTs(ctx context.Context, address string) ([]models.NFT, error) {
	request, err := http.NewRequestWithContext(ctx, http.MethodGet, URL+"/v0/nfts/"+address, http.NoBody)
	if err != nil {
		return nil, err
	}

	query := request.URL.Query()
	query.Add("chain", "rinkeby")
	query.Add("page_number", "1")
	query.Add("page_size", "20")
	request.URL.RawQuery = query.Encode()
	request.Header.Add("Authorization", c.apiKey)

	response, err := c.httpClient.Do(request)
	if err != nil {
		return nil, err
	}

	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return nil, ErrUnknown
	}

	body, err := io.ReadAll(response.Body)
	if err != nil {
		return nil, err
	}

	var result struct {
		NFTs []struct {
			ContractAddress string `json:"contract_address"`
			TokenID         string `json:"token_id"`
		} `json:"nfts"`
		Response string `json:"response"`
	}

	if err := json.Unmarshal(body, &result); err != nil {
		return nil, err
	}

	if result.Response != StatusOK {
		return nil, ErrUnknown
	}

	nfts := make([]models.NFT, 0, len(result.NFTs))

	for _, nft := range result.NFTs {
		nfts = append(nfts, models.NFT{
			ContractAddress: nft.ContractAddress,
			TokenID:         nft.TokenID,
		})
	}

	return nfts, nil
}
