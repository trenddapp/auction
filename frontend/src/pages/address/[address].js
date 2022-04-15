import { useRouter } from 'next/router'
import { useEffect } from 'react'
import Asset from '../../components/Asset/Asset'

// TODO: Remove me!
const NFTs = [
  {
    id: '0',
    contractAddress: '0x94b1bd2a4acfa531c8c330c389072cb08db28108',
    from: '0x9cdb45dd263327416118778b927c9050a3461c30',
    to: '0xd524a5c8c6b8bb81e6d1a1fe8b2959cc6b342bae',
    tokenId: '70948226068845075091097172684116137139687598325071419309035027374095581839367',
  },
  {
    id: '1',
    contractAddress: '0x94b1bd2a4acfa531c8c330c389072cb08db28108',
    from: '0x9cdb45dd263327416118778b927c9050a3461c30',
    to: '0xd524a5c8c6b8bb81e6d1a1fe8b2959cc6b342bae',
    tokenId: '70948226068845075091097172684116137139687598325071419309035027374095581839366',
  },
]

const Address = () => {
  const router = useRouter()
  const { address } = router.query

  useEffect(() => {
    // TODO: Fetch assets based on wallet address.
  }, [])

  const assets = NFTs.map((nft) => {
    return <Asset asset={nft} key={nft.id} />
  })

  return <>{assets}</>
}

export default Address
