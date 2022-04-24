import Head from 'next/head'

import { Banner } from '../components/Banner'
import { Nav } from '../components/Nav'
import { Terms } from '../components/Terms'

const HomePage = () => {
  return (
    <>
      <Head>
        <title>Auction</title>
        <meta name="description" content="Decentralized Auction by DAPP-Z" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Banner />
      <Nav />
      <Terms />
    </>
  )
}

export default HomePage
