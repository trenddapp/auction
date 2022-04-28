import { useMemo } from 'react'

import { ethers } from 'ethers'

import { abiAuction } from '../config/abi'
import addresses from '../config/constants/addresses'
import useWeb3ChainId from './useWeb3ChainId'
import useWeb3Provider from './useWeb3Provider'

const useContractAuction = (signer) => {
  const address = addresses.auction[useWeb3ChainId()]
  const provider = useWeb3Provider()

  try {
    if (signer === undefined) {
      return useMemo(() => new ethers.Contract(address, abiAuction, provider), [provider])
    }

    return useMemo(() => new ethers.Contract(address, abiAuction, signer), [signer])
  } catch (error) {
    return undefined
  }
}

export default useContractAuction
