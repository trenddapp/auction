export const getEtherscanUrl = (address) => {
  return 'https://rinkeby.etherscan.io/address/' + address
}

export const shortenAddress = (address) => {
  if (address.length !== 42) {
    return '0x0...000'
  }

  return `${address.slice(0, 3)}...${address.slice(39, 42)}`
}

export const shortenTokenId = (tokenId) => {
  if (tokenId.length <= 8) {
    return tokenId
  }

  return tokenId.slice(0, 2) + '...' + tokenId.slice(tokenId.length - 3, tokenId.length)
}
