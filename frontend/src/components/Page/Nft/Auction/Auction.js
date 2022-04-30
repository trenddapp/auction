import { useEffect, useState } from 'react'

import styled from 'styled-components'

import { Flex, Text } from '../../../Toolkit'
import { useWeb3Profile } from '../../../../hooks'
import BidForm from './BidForm'
import CreateForm from './CreateForm'
import EditForm from './EditForm'
import Header from './Header'
import Information from './Information'

const Container = styled(Flex)`
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  flex-direction: column;
  height: 500px;
  justify-content: space-between;
  padding: 16px;
  width: 400px;

  ${({ theme }) => theme.mediaQueries.sm} {
    width: 500px;
  }

  ${({ theme }) => theme.mediaQueries.lg} {
    width: 100%;
  }
`

const Auction = ({ auction, contractAddress, nft, tokenId }) => {
  const [isOwner, setIsOwner] = useState(false)

  const { account } = useWeb3Profile()

  useEffect(() => {
    setIsOwner(account !== undefined && nft.owner !== undefined && account === nft.owner)
  }, [account, nft.owner])

  if (auction.error !== undefined) {
    return (
      <Container>
        <Header isOwner={isOwner} nft={nft} />
        <Text>Oops! Something went wrong.</Text>
      </Container>
    )
  }

  if (auction.isLoading) {
    return (
      <Container>
        <Header isOwner={isOwner} nft={nft} />
        <Text>Loading...</Text>
      </Container>
    )
  }

  if (auction.isAvailable && isOwner) {
    return (
      <Container>
        <Header isOwner={isOwner} nft={nft} />
        <Flex flexDirection="column">
          <Information auction={auction} />
          <EditForm auction={auction} contractAddress={contractAddress} tokenId={tokenId} />
        </Flex>
      </Container>
    )
  }

  if (auction.isAvailable && !isOwner) {
    return (
      <Container>
        <Header isOwner={isOwner} nft={nft} />
        <Flex flexDirection="column">
          <Information auction={auction} />
          <BidForm auction={auction} contractAddress={contractAddress} tokenId={tokenId} />
        </Flex>
      </Container>
    )
  }

  if (!auction.isAvailable && isOwner) {
    return (
      <Container>
        <Header isOwner={isOwner} nft={nft} />
        <CreateForm contractAddress={contractAddress} tokenId={tokenId} />
      </Container>
    )
  }

  if (!auction.isAvailable && !isOwner) {
    return (
      <Container>
        <Header isOwner={isOwner} nft={nft} />
        <Text>Ahh, no auction found!</Text>
      </Container>
    )
  }

  return null
}

export default Auction
