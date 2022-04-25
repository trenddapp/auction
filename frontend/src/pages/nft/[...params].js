import { useRouter } from 'next/router'
import Head from 'next/head'

import styled, { useTheme } from 'styled-components'

import { Banner } from '../../components/Banner'
import { Flex, Text } from '../../components/Toolkit'
import { Nav } from '../../components/Nav'
import { shortenAddress } from '../../utils'
import { SvgPhotograph } from '../../components/Svg'
import { Terms } from '../../components/Terms'
import { useNft } from '../../hooks'

const Container = styled(Flex)`
  align-items: center;
  flex-direction: column;
  height: 100%;
  margin: 0 auto;
  max-width: ${({ theme }) => `${theme.siteWidth}px`};
  padding: 16px;

  ${({ theme }) => theme.mediaQueries.sm} {
    border-left: 1px dashed ${({ theme }) => theme.colors.borderAlt};
    border-right: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  }

  ${({ theme }) => theme.mediaQueries.lg} {
    align-items: flex-start;
    flex-direction: row;
  }
`

const Details = styled(Flex)`
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  flex-direction: column;
  margin-top: 16px;
  padding: 16px;
  width: 400px;

  ${({ theme }) => theme.mediaQueries.sm} {
    width: 500px;
  }
`

const File = styled(Flex)`
  align-items: center;
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  height: 400px;
  justify-content: center;
  overflow: hidden;
  padding: 16px;
  width: 400px;

  ${({ theme }) => theme.mediaQueries.sm} {
    height: 500px;
    width: 500px;
  }
`

const Metadata = styled(Flex)`
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  flex-direction: column;
  height: 658px;
  margin: 16px 0 0 0;
  padding: 16px;
  width: 400px;

  ${({ theme }) => theme.mediaQueries.sm} {
    width: 500px;
  }

  ${({ theme }) => theme.mediaQueries.lg} {
    margin: 0 0 0 16px;
    width: 100%;
  }
`

const Section = styled.section`
  background-color: ${({ theme }) => theme.colors.background};
  border-top: 1px solid ${({ theme }) => theme.colors.border};
  padding: 0 16px;
`

const NftPage = () => {
  const theme = useTheme()

  const router = useRouter()
  const {
    params: [contractAddress, tokenId],
  } = router.query

  const { error, image, isLoading, metadata } = useNft(contractAddress, tokenId)

  return (
    <>
      <Head>
        <title>Auction | NFT</title>
        <meta name="description" content="Decentralized Auction by DAPP-Z" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Banner />
      <Nav />
      <Section>
        <Container>
          <Flex alignItems="center" flexDirection="column" justifyContent="center">
            <File>
              {error !== undefined ? (
                <Flex alignItems="center" flexDirection="column" justifyContent="center">
                  <Text>Oops!</Text>
                  <Text as="span">Something went wrong.</Text>
                </Flex>
              ) : isLoading ? (
                <SvgPhotograph height="60px" width="60px" />
              ) : (
                <img src={image} alt="icons" />
              )}
            </File>
            <Details>
              <Flex alignItems="center" justifyContent="space-between">
                <Text>Blockchain:</Text>
                <Text as="span">Rinkeby</Text>
              </Flex>
              <Flex alignItems="center" justifyContent="space-between" marginTop="4px">
                <Text>Contract Address:</Text>
                <Text as="span">{shortenAddress(contractAddress)}</Text>
              </Flex>
              <Flex alignItems="center" justifyContent="space-between" marginTop="4px">
                <Text>Token ID:</Text>
                <Text as="span">
                  {tokenId.length <= 8
                    ? tokenId
                    : tokenId.slice(0, 2) + '...' + tokenId.slice(tokenId.length - 3, tokenId.length)}
                </Text>
              </Flex>
              <Flex alignItems="center" justifyContent="space-between" marginTop="4px">
                <Text>Token Standard:</Text>
                <Text as="span">ERC-721</Text>
              </Flex>
            </Details>
          </Flex>
          <Metadata>
            <Text color={theme.colors.headline} fontSize="36px">
              {error !== undefined ? 'NOT FOUND' : isLoading ? 'NAME' : metadata.name}
            </Text>
          </Metadata>
        </Container>
      </Section>
      <Terms />
    </>
  )
}

export default NftPage
