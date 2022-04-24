import Link from 'next/link'

import styled from 'styled-components'

import { Flex, Text } from '../../components/Toolkit'
import { SvgPhotograph } from '../../components/Svg'
import { useNft } from '../../hooks'

const Container = styled(Flex)`
  align-items: center;
  border: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  border-radius: ${({ theme }) => theme.radii.normal};
  flex-direction: column;
  justify-content: flex-start;
  margin: 8px;
  padding: 16px;

  &:hover {
    border: 1px solid ${({ theme }) => theme.colors.borderAlt};
  }
`

const Details = styled(Flex)`
  border-top: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  flex-direction: column;
  margin-top: 16px;
  padding-top: 8px;
  width: 100%;
`

const Image = styled(Flex)`
  align-items: center;
  height: 250px;
  justify-content: center;
  overflow: hidden;
  width: 250px;
`

const TokenId = styled(Text)`
  color: ${({ theme }) => theme.colors.action};
  cursor: pointer;
`

const Asset = ({ contractAddress, tokenId }) => {
  const { error, image, isLoading } = useNft(contractAddress, tokenId)

  return (
    <Container>
      <Image>
        {isLoading ? (
          <SvgPhotograph height="50px" width="50px" />
        ) : error !== undefined ? (
          <Flex alignItems="center" flexDirection="column" justifyContent="center">
            <Text>Oops!</Text>
            <Text as="span">Something went wrong.</Text>
          </Flex>
        ) : (
          <img src={image} alt="icons" />
        )}
      </Image>
      <Details>
        <Flex>
          <Link href={`/nft/${contractAddress}/${tokenId}`}>
            <TokenId>
              #
              {tokenId.length <= 8
                ? tokenId
                : tokenId.slice(0, 2) + '...' + tokenId.slice(tokenId.length - 3, tokenId.length)}
            </TokenId>
          </Link>
        </Flex>
      </Details>
    </Container>
  )
}

export default Asset
