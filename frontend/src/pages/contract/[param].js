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
  flex-direction: row;
  flex-wrap: wrap;
  height: 100%;
  justify-content: space-around;
  margin: 0 auto;
  max-width: ${({ theme }) => `${theme.siteWidth}px`};
  padding: 16px;

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

const Contract = () => {
  const [error, setError] = useState()
  const [isLoading, setIsLoading] = useState(true)
  const [nfts, setNfts] = useState()

  const router = useRouter()
  const { param: address } = router.query

  useEffect(() => {
    const fetchNfts = async () => {
      const nftsUri = `https://127.0.0.1:9080/nft/contract/${address}`
      const nftsRaw = await fetch(nftsUri)
      const nftsJson = await nftsRaw.json()
      setNfts(nftsJson.nfts)
      setIsLoading(false)
    }

    fetchNfts().catch((error) => setError(`ContractPage component: ${error}`))
  }, [address])

  return (
    <>
      <Head>
        <title>Auction | Contract</title>
        <meta name="description" content="Decentralized Auction by DAPP-Z" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Banner />
      <Nav />
      <Section>
        <Container>
          {error !== undefined ? (
            <Text>Oops! Something went wrong.</Text>
          ) : isLoading ? (
            <Text>Loading...</Text>
          ) : (
            nfts.map((nft) => <Asset contractAddress={nft.ContractAddress} key={nft.TokenID} tokenId={nft.TokenID} />)
          )}
        </Container>
      </Section>
      <Terms />
    </>
  )
}

export default Contract
