import { useEffect, useState } from 'react'

import useContractNft from './useContractNft'

const useNft = (contractAddress, tokenId) => {
  const [error, setError] = useState()
  const [image, setImage] = useState()
  const [isLoading, setIsLoading] = useState(true)
  const [metadata, setMetadata] = useState()
  const [owner, setOwner] = useState()
  const contractNft = useContractNft(contractAddress, undefined)

  useEffect(() => {
    if (contractNft === undefined) {
      setError('useNft hook: undefined nft contract')
      return
    }

    const fetchNft = async () => {
      const metadataCid = await contractNft.tokenURI(tokenId)

      let metadataUri = `https://ipfs.io/ipfs/${metadataCid}`
      if (metadataCid.startsWith('ipfs://')) {
        metadataUri = `https://ipfs.io/ipfs/${metadataCid.replace('ipfs://', '')}`
      }

      const metadataRaw = await fetch(metadataUri)
      const metadataJson = await metadataRaw.json()
      setMetadata(metadataJson)

      let imageUri = `https://ipfs.io/ipfs/${metadataJson.image}`
      if (metadataJson.image.startsWith('ipfs://')) {
        imageUri = `https://ipfs.io/ipfs/${metadataJson.image.replace('ipfs://', '')}`
      }

      const imageRaw = await fetch(imageUri)
      const imageBlob = await imageRaw.blob()
      setImage(URL.createObjectURL(imageBlob))

      const owner = await contractNft.ownerOf(tokenId)
      setOwner(owner)

      setIsLoading(false)
    }

    fetchNft().catch((error) => setError(`useNft hook: ${error}`))
  }, [])

  return {
    error,
    image,
    isLoading,
    metadata,
    owner,
  }
}

export default useNft
