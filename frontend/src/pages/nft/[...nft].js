import { useRouter } from 'next/router'

const Nft = () => {
  const router = useRouter()

  // The first element is the contract address.
  // The second element is the token id.
  const { nft } = router.query
  if (nft.length !== 2) {
    // TODO: Return 404 page.
  }

  return <div>NFT Page</div>
}

export default Nft
