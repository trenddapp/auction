import { useMemo } from 'react'
import { ethers } from 'ethers'
import { abiNft } from '../config/abi'
import useWeb3Provider from './useWeb3Provider'

const useContractNft = (contractAddress) => {
  const provider = useWeb3Provider()

  try {
    return useMemo(() => new ethers.Contract(contractAddress, abiNft, provider), [contractAddress, provider])
  } catch (error) {
    return undefined
  }
}

export default useContractNft
