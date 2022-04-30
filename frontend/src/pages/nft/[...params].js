import { useRouter } from 'next/router'

import styled from 'styled-components'

import { Flex } from '../../components/Toolkit'
import { NftBase, NftDetails, NftFile, NftAuction, NftTimer } from '../../components/Page/Nft'
import { useAuction, useNft } from '../../hooks'

const Left = styled(Flex)`
  flex-direction: column;
`

const Right = styled(Flex)`
  flex-direction: column;
  margin: 16px 0 0 0;
  width: auto;

  ${({ theme }) => theme.mediaQueries.lg} {
    margin: 0 0 0 16px;
    width: 100%;
  }
`

const NftPage = () => {
  const router = useRouter()
  const {
    params: [contractAddress, tokenId],
  } = router.query

  const auction = useAuction(contractAddress, tokenId)
  const nft = useNft(contractAddress, tokenId)

  return (
    <NftBase>
      <Left>
        <NftFile error={nft.error} isLoading={nft.isLoading} image={nft.image} />
        <NftDetails blockchain="Rinkeby" contractAddress={contractAddress} tokenId={tokenId} tokenStandard="ERC-721" />
      </Left>
      <Right>
        <NftAuction auction={auction} contractAddress={contractAddress} nft={nft} tokenId={tokenId} />
        <NftTimer endDate={auction.endDate} />
      </Right>
    </NftBase>
  )
}

export default NftPage
