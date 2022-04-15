import { useEffect } from 'react'

const Asset = ({ asset }) => {
  useEffect(() => {
    // TODO: Fetch  the asset uri.
    // TODO: Fetch the asset.
  }, [])

  return <p>{asset.tokenId}</p>
}

export default Asset
