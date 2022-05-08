import Head from 'next/head'

import styled from 'styled-components'

import { Banner } from '../../../Banner'
import { Flex } from '../../../Toolkit'
import { Nav } from '../../../Nav'
import { Terms } from '../../../Terms'

const Container = styled(Flex)`
  flex-wrap: wrap;
  justify-content: space-around;
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

const Base = ({ children }) => {
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
        <Container>{children}</Container>
      </Section>
      <Terms />
    </>
  )
}

export default Base
