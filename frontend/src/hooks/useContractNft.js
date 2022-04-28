import { useMemo } from 'react'

import { ethers } from 'ethers'

import { abiNft } from '../config/abi'
import useWeb3Provider from './useWeb3Provider'

const useContractNft = (contractAddress, signer) => {
  const provider = useWeb3Provider()

  try {
    if (signer === undefined) {
      return useMemo(() => new ethers.Contract(contractAddress, abiNft, provider), [contractAddress, provider])
    }

    return useMemo(() => new ethers.Contract(contractAddress, abiNft, signer), [contractAddress, signer])
  } catch (error) {
    return undefined
  }
}

export default useContractNft
