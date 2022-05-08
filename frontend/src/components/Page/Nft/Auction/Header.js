import styled from 'styled-components'

import { Box, Flex, Text } from '../../../Toolkit'
import { getEtherscanUrl, shortenAddress } from '../../../../utils'
import { SvgExternalLink } from '../../../Svg'

const Clickable = styled(Text)`
  color: ${({ theme }) => theme.colors.action};
  cursor: pointer;
  display: flex;
`

const Container = styled(Flex)`
  flex-direction: column;
`

const Headline = styled(Flex)`
  color: ${({ theme }) => theme.colors.headline};
  font-size: 36px;
`

const Header = ({ isOwner, nft }) => {
  return (
    <Container>
      <Headline>{nft.error !== undefined ? 'NOT FOUND' : nft.isLoading ? 'NAME' : nft.metadata.name}</Headline>
      <Flex alignItems="center">
        <Text marginRight="4px">Owned by </Text>
        {nft.error !== undefined ? (
          <Text>NOT FOUND</Text>
        ) : nft.isLoading ? (
          <Text>0x0...000</Text>
        ) : (
          <Clickable as="a" href={getEtherscanUrl(nft.owner)} target="_blank">
            {isOwner ? 'you' : shortenAddress(nft.owner)}
            <Box marginLeft="3px">
              <SvgExternalLink height="12px" width="12px" />
            </Box>
          </Clickable>
        )}
      </Flex>
    </Container>
  )
}

export default Header
