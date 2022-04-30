import { useState } from 'react'

import dayjs from 'dayjs'
import styled from 'styled-components'

import { Flex, Text } from '../../../Toolkit'
import { useContractAuction, useContractNft, useWeb3Signer } from '../../../../hooks'
import addresses from '../../../../config/constants/addresses'

const Button = styled.button`
  background: ${({ theme }) => theme.colors.action};
  border-radius: ${({ theme }) => theme.radii.small};
  border: none;
  color: ${({ theme }) => theme.colors.background};
  margin-top: 32px;
  padding: 12px 11px 12px 11px;

  &:hover {
    cursor: pointer;
  }
`

const Input = styled.input`
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px solid ${({ theme }) => theme.colors.borderAlt};
  color: ${({ theme }) => theme.colors.text};
  padding: 12px 11px 10px 11px;
  margin-top: 2px;

  &:focus {
    outline: none;
  }
`

const Label = styled(Text)`
  font-weight: 600;
  margin-bottom: 2px;
`

const CreateForm = ({ contractAddress, tokenId }) => {
  const [inputs, setInputs] = useState({
    duration: 0,
    end: dayjs().add(7, 'day').format('YYYY-MM-DD'),
    price: 0,
    start: dayjs().format('YYYY-MM-DD'),
  })

  const signer = useWeb3Signer()
  const contractAuction = useContractAuction(signer)
  const contractNft = useContractNft(contractAddress, signer)

  const handleInputChange = (e) => {
    setInputs({
      ...inputs,
      [e.target.name]: e.target.value,
    })
  }

  const handleCreateAuction = async () => {
    if (contractAuction === undefined || contractNft === undefined) {
      return
    }

    try {
      const approvedAddress = await contractNft.getApproved(tokenId)

      if (approvedAddress !== contractAuction.address) {
        await contractNft.approve(addresses.proxy.auction['4'], tokenId)
      }

      await contractAuction.createAuction(
        contractAddress,
        tokenId,
        inputs.price,
        dayjs(inputs.start, 'YYYY-MM-DD').unix(),
        dayjs(inputs.end, 'YYYY-MM-DD').unix(),
      )
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <Flex flexDirection="column">
      <Flex flexDirection="column">
        <Label>Price</Label>
        <Input name="price" onChange={handleInputChange} type="number" value={inputs.price} />
      </Flex>

      <Flex flexDirection="column" marginTop="16px">
        <Label>Duration</Label>
        <Input name="duration" onChange={handleInputChange} type="number" value={inputs.duration} />
      </Flex>

      <Flex alignItems="center" justifyContent="space-between" marginTop="16px" width="100%">
        <Flex flexDirection="column" width="calc(100%/2 - 8px)">
          <Label>Start</Label>
          <Input name="start" onChange={handleInputChange} type="date" value={inputs.start} />
        </Flex>
        <Flex flexDirection="column" width="calc(100%/2 - 8px)">
          <Label>End</Label>
          <Input name="end" onChange={handleInputChange} type="date" value={inputs.end} />
        </Flex>
      </Flex>

      <Button onClick={handleCreateAuction}>Create Auction</Button>
    </Flex>
  )
}

export default CreateForm
