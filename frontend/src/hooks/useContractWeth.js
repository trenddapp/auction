import { useMemo } from 'react'

import { ethers } from 'ethers'

import { abiWeth } from '../config/abi'
import addresses from '../config/constants/addresses'
import useWeb3ChainId from './useWeb3ChainId'
import useWeb3Provider from './useWeb3Profile'

const useContractWeth = (signer) => {
  const address = addresses.original.weth[useWeb3ChainId()]
  const provider = useWeb3Provider()

  try {
    if (signer === undefined) {
      return useMemo(() => new ethers.Contract(address, abiWeth, provider), [provider])
    }

    return useMemo(() => new ethers.Contract(address, abiWeth, signer), [signer])
  } catch (error) {
    return undefined
  }
}

export default useContractWeth
