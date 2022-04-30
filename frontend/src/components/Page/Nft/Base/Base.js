import Head from 'next/head'

import styled from 'styled-components'

import { Banner } from '../../../Banner'
import { Flex } from '../../../Toolkit'
import { Nav } from '../../../Nav'
import { Terms } from '../../../Terms'

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

const Section = styled.section`
  background-color: ${({ theme }) => theme.colors.background};
  border-top: 1px solid ${({ theme }) => theme.colors.border};
  padding: 0 16px;
`

const Base = ({ children }) => {
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
        <Container>{children}</Container>
      </Section>
      <Terms />
    </>
  )
}

export default Base
