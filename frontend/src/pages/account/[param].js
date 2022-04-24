import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'

import styled from 'styled-components'

import { Asset } from '../../components/Asset'
import { Banner } from '../../components/Banner'
import { Flex, Text } from '../../components/Toolkit'
import { Nav } from '../../components/Nav'
import { Terms } from '../../components/Terms'

const Container = styled(Flex)`
  align-items: flex-start;
  flex-wrap: wrap;
  justify-content: space-between;
  margin: 0 auto;
  max-width: ${({ theme }) => `${theme.siteWidth}px`};

  /* Banner: 30px, Nav: 84px, Terms: 50px */
  min-height: calc(100vh - 30px - 84px - 50px - 1px);
  padding: 8px;

  ${({ theme }) => theme.mediaQueries.sm} {
    border-left: 1px dashed ${({ theme }) => theme.colors.borderAlt};
    border-right: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  }
`

const Section = styled.section`
  background-color: ${({ theme }) => theme.colors.background};
  border-top: 1px solid ${({ theme }) => theme.colors.border};
  padding: 0 16px;
`

const AccountPage = () => {
  const [error, setError] = useState()
  const [isLoading, setIsLoading] = useState(true)
  const [nfts, setNfts] = useState()

  const router = useRouter()
  const { param: address } = router.query

  useEffect(async () => {
    try {
      const nftsUri = `http://127.0.0.1:9080/nft/account/${address}`
      const nftsRaw = await fetch(nftsUri)
      const nftsJson = await nftsRaw.json()
      setNfts(nftsJson.nfts)
    } catch (error) {
      setError(`AccountPage component: ${error}`)
    }

    setIsLoading(false)
  }, [])

  return (
    <>
      <Head>
        <title>Auction | Account</title>
        <meta name="description" content="Decentralized Auction by DAPP-Z" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Banner />
      <Nav />
      <Section>
        <Container>
          {isLoading ? (
            <Text>Loading...</Text>
          ) : error !== undefined ? (
            <Text>Oops! Something went wrong.</Text>
          ) : (
            nfts.map((nft) => (
              <Asset
                contractAddress={nft.ContractAddress}
                key={nft.ContractAddress + nft.TokenID}
                tokenId={nft.TokenID}
              />
            ))
          )}
        </Container>
      </Section>
      <Terms />
    </>
  )
}

export default AccountPage
