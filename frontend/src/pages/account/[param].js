import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'

import { AccountBase } from '../../components/Page/Account'
import { Asset } from '../../components/Asset'
import { Text } from '../../components/Toolkit'

const AccountPage = () => {
  const [error, setError] = useState()
  const [isLoading, setIsLoading] = useState(true)
  const [nfts, setNfts] = useState()

  const router = useRouter()
  const { param: address } = router.query

  useEffect(() => {
    if (!router.isReady) {
      return
    }

    const fetchNfts = async () => {
      const nftsUri = `https://dappz-auction.herokuapp.com/nft/account/${address}`
      const nftsRaw = await fetch(nftsUri)
      const nftsJson = await nftsRaw.json()
      setNfts(nftsJson.nfts)
      setIsLoading(false)
    }

    try {
      fetchNfts()
    } catch (error) {
      setError(`AccountPage component: ${error}`)
    }
  }, [address, router.isReady])

  return (
    <AccountBase>
      {error !== undefined ? (
        <Text>Oops! Something went wrong.</Text>
      ) : isLoading ? (
        <Text>Loading...</Text>
      ) : (
        nfts.map((nft) => (
          <Asset contractAddress={nft.ContractAddress} key={nft.ContractAddress + nft.TokenID} tokenId={nft.TokenID} />
        ))
      )}
    </AccountBase>
  )
}

export default AccountPage
