import styled from 'styled-components'

import { Box, Flex, Text } from '../../../Toolkit'
import { getEtherscanUrl, shortenAddress, shortenTokenId } from '../../../../utils'
import { SvgExternalLink } from '../../../Svg'

const Clickable = styled(Text)`
  color: ${({ theme }) => theme.colors.action};
  cursor: pointer;
  display: flex;
`

const Container = styled(Flex)`
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  flex-direction: column;
  margin-top: 16px;
  padding: 16px;
  width: 400px;

  ${({ theme }) => theme.mediaQueries.sm} {
    width: 500px;
  }
`

const Item = styled(Flex)`
  align-items: center;
  justify-content: space-between;
`

const Details = ({ blockchain, contractAddress, tokenId, tokenStandard }) => {
  return (
    <Container>
      <Item>
        <Text>Blockchain:</Text>
        <Text>{blockchain}</Text>
      </Item>
      <Item marginTop="4px">
        <Text>Contract Address:</Text>
        <Clickable as="a" href={getEtherscanUrl(contractAddress)} target="_blank">
          {shortenAddress(contractAddress)}
          <Box marginLeft="2px">
            <SvgExternalLink height="12px" width="12px" />
          </Box>
        </Clickable>
      </Item>
      <Item marginTop="4px">
        <Text>Token ID:</Text>
        <Text>{shortenTokenId(tokenId)}</Text>
      </Item>
      <Item marginTop="4px">
        <Text>Token Standard:</Text>
        <Text>{tokenStandard}</Text>
      </Item>
    </Container>
  )
}

export default Details
