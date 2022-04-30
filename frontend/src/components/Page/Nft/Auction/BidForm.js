import { useState } from 'react'

import { ethers } from 'ethers'
import styled from 'styled-components'

import { Flex, Text } from '../../../Toolkit'
import { useContractAuction, useContractWeth, useToast, useWeb3Profile, useWeb3Signer } from '../../../../hooks'

const Button = styled.button`
  background: ${({ theme }) => theme.colors.action};
  border-radius: ${({ theme }) => theme.radii.small};
  border: none;
  color: ${({ theme }) => theme.colors.background};
  margin-top: 16px;
  padding: 12px 11px;

  &:hover {
    cursor: pointer;
  }
`

const Container = styled(Flex)`
  flex-direction: column;
  margin-top: 16px;
`

const Input = styled.input`
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px solid ${({ theme }) => theme.colors.borderAlt};
  color: ${({ theme }) => theme.colors.text};
  padding: 12px 11px 10px;

  &:focus {
    outline: none;
  }
`

const Label = styled(Text)`
  font-weight: 600;
  margin-bottom: 4px;
`

const BidForm = ({ auction, contractAddress, tokenId }) => {
  const { highestBid, price } = auction

  const [error, setError] = useState()
  const [inputs, setInputs] = useState({
    price: highestBid > price ? highestBid : price,
  })

  const { account } = useWeb3Profile()
  const { toastError, toastInfo, toastSuccess } = useToast()
  const contractAuction = useContractAuction(useWeb3Signer())
  const contractWeth = useContractWeth(useWeb3Signer())

  const handleButtonClick = async (e) => {
    switch (e.target.name) {
      case 'bid':
        if (contractAuction === undefined) {
          setError(`Bid component: ${error}`)
          toastError('Failed to bid', 'Sorry, please try again later!')
          break
        }

        try {
          const allowedAmount = await contractWeth.allowance(account, contractAuction.address)
          if (inputs.price !== allowedAmount) {
            const transaction = await contractWeth.approve(contractAuction.address, inputs.price.toNumber())
            const receipt = await transaction.wait()

            if (!receipt.status) {
              throw new Error('Failed to approve weth')
            }

            toastInfo('Wait for it!', 'You gotta wait for the next transaction.')
          }

          const transaction = await contractAuction.bid(contractAddress, tokenId, inputs.price.toNumber())
          const receipt = await transaction.wait()

          if (!receipt.status) {
            throw new Error('Failed to bid')
          }

          toastSuccess('Successful Transaction', 'We hope you get the NFT!')
        } catch (error) {
          setError(error)
          toastError('Failed to bid', `${error}`)
        }

        break
    }
  }

  const handleInputChange = (e) => {
    switch (e.target.name) {
      case 'price':
        setInputs({
          ...inputs,
          price: ethers.BigNumber.from(e.target.value),
        })
        break
      default:
        setInputs({
          ...inputs,
          [e.target.name]: e.target.value,
        })
    }
  }

  return (
    <Container>
      <Flex flexDirection="column">
        <Label>Price</Label>
        <Input name="price" onChange={handleInputChange} type="number" value={inputs.price.toNumber()} />
      </Flex>
      <Button name="bid" onClick={handleButtonClick}>
        Bid
      </Button>
    </Container>
  )
}

export default BidForm
