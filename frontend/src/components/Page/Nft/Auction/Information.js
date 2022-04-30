import styled from 'styled-components'

import { Flex, Text } from '../../../Toolkit'
import { shortenAddress } from '../../../../utils'

const Container = styled(Flex)`
  flex-direction: column;
`

const Item = styled(Flex)`
  justify-content: space-between;
`

const Label = styled(Text)`
  font-weight: 600;
`

const Value = styled(Text)``

const Information = ({ auction }) => {
  const { highestBid, highestBidder, price } = auction

  return (
    <Container>
      <Item>
        <Label>Price:</Label>
        <Value>{price.toString()}</Value>
      </Item>
      <Item marginTop="8px">
        <Label>Highest Bid:</Label>
        <Value>{highestBid.toString()}</Value>
      </Item>
      <Item marginTop="8px">
        <Label>Highest Bidder:</Label>
        <Value>{shortenAddress(highestBidder)}</Value>
      </Item>
    </Container>
  )
}

export default Information
