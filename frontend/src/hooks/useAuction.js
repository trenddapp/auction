import { useEffect, useState } from 'react'

import useContractAuction from './useContractAuction'

const useAuction = (contractAddress, tokenId) => {
  const [endDate, setEndDate] = useState()
  const [error, setError] = useState()
  const [highestBid, setHighestBid] = useState()
  const [highestBidder, setHighestBidder] = useState()
  const [isAvailable, setIsAvailable] = useState()
  const [isLoading, setIsLoading] = useState(true)
  const [price, setPrice] = useState()
  const [startDate, setStartDate] = useState()

  const contractAuction = useContractAuction(undefined)

  useEffect(() => {
    if (contractAuction === undefined) {
      setError('useAuction hook: undefined auction contract')
    }

    const fetchAuction = async () => {
      const auction = await contractAuction.allAuctions(contractAddress, tokenId)

      setEndDate(new Date(auction.endingTimestamp.toNumber() * 1000))
      setHighestBid(auction.highestBid)
      setHighestBidder(auction.highestBidder)
      setIsAvailable(auction.startingTimestamp.toNumber() !== 0)
      setPrice(auction.startingPrice)
      setStartDate(new Date(auction.startingTimestamp.toNumber() * 1000))
      setIsLoading(false)
    }

    fetchAuction().catch((error) => setError(`useAuction hook: ${error}`))
  }, [])

  return {
    endDate,
    error,
    highestBid,
    highestBidder,
    isAvailable,
    isLoading,
    startDate,
    price,
  }
}

export default useAuction
