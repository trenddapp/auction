package etherscan

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"net/http"

	"github.com/dapp-z/auction/backend/service/nft/models"
)

const (
	StatusOK = "1"
	URL      = "https://api-rinkeby.etherscan.io/api"
)

var (
	ErrUnknown = errors.New("unknown error")
)

type client struct {
	apiKey     string
	httpClient *http.Client
}

// NewClient returns a client that implements the Client interface.
func NewClient(config *Config) Client {
	return &client{
		apiKey:     config.APIKey,
		httpClient: http.DefaultClient,
	}
}

func (c *client) GetNFTsByWalletAddress(ctx context.Context, address string) ([]models.NFT, error) {
	request, err := http.NewRequestWithContext(ctx, http.MethodGet, URL+"", http.NoBody)
	if err != nil {
		return nil, err
	}

	query := request.URL.Query()
	query.Add("action", "tokennfttx")
	query.Add("address", address)
	query.Add("apikey", c.apiKey)
	query.Add("module", "account")
	request.URL.RawQuery = query.Encode()

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
		Status string `json:"status"`

		// Result is an array when status is ok.
		// Result is a string when status is non-ok.
		Result json.RawMessage `json:"result"`
	}

	if err := json.Unmarshal(body, &result); err != nil {
		return nil, err
	}

	if result.Status != StatusOK {
		var message string

		if err := json.Unmarshal(result.Result, &message); err != nil {
			return nil, err
		}

		return nil, errors.New(message)
	}

	var transactions []struct {
		ContractAddress string `json:"contractAddress"`
		From            string `json:"from"`
		To              string `json:"to"`
		TokenID         string `json:"tokenID"`
		TokenName       string `json:"tokenName"`
		TokenSymbol     string `json:"tokenSymbol"`
	}

	if err := json.Unmarshal(result.Result, &transactions); err != nil {
		return nil, err
	}

	nfts := make([]models.NFT, 0, len(transactions))

	for _, transaction := range transactions {
		nfts = append(nfts, models.NFT{
			ContractAddress: transaction.ContractAddress,
			From:            transaction.From,
			To:              transaction.To,
			TokenID:         transaction.TokenID,
		})
	}

	return nfts, nil
}
