import { useState } from 'react'

import { ethers } from 'ethers'
import dayjs from 'dayjs'
import styled from 'styled-components'

import { Flex, Text } from '../../../Toolkit'
import { useContractAuction, useToast, useWeb3Signer } from '../../../../hooks'

const Container = styled(Flex)`
  flex-direction: column;
  margin-top: 16px;
`

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

const EditForm = ({ auction, contractAddress, tokenId }) => {
  const { endDate, price } = auction

  const [error, setError] = useState()
  const [inputs, setInputs] = useState({
    endDate: endDate,
    price: price,
  })

  const { toastError, toastSuccess } = useToast()
  const contractAuction = useContractAuction(useWeb3Signer())

  const handleButtonClick = async (e) => {
    switch (e.target.name) {
      case 'updateAuction':
        if (contractAuction === undefined) {
          setError(`Edit component: ${error}`)
          toastError('Failed to update', 'Sorry, please try again later.')
          break
        }

        try {
          if (inputs.endDate !== endDate) {
            await contractAuction.updateEndingTimestamp(contractAddress, tokenId, inputs.endDate.unix())
            toastSuccess('Successful transaction!', 'Ending timestamp updated successfully.')
          }

          if (inputs.price !== price) {
            await contractAuction.updateStartingPrice(contractAddress, tokenId, inputs.price.toNumber())
            toastSuccess('Successful transaction!', 'Starting price updated successfully.')
          }
        } catch (error) {
          setError(error)
          toastError('Failed to update', `${error}`)
        }

        break
    }
  }

  const handleInputChange = (e) => {
    switch (e.target.name) {
      case 'endDate':
        setInputs({
          ...inputs,
          endDate: dayjs(e.target.value, 'YYYY-MM-DD'),
        })
        break
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
      <Flex flexDirection="column" marginTop="8px">
        <Label>End</Label>
        <Input
          name="endDate"
          onChange={handleInputChange}
          type="date"
          value={dayjs(inputs.endDate).format('YYYY-MM-DD')}
        />
      </Flex>
      <Button name="updateAuction" onClick={handleButtonClick}>
        Update Auction
      </Button>
    </Container>
  )
}

export default EditForm
