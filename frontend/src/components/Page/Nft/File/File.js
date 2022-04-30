import styled from 'styled-components'

import { Flex, Text } from '../../../Toolkit'
import { SvgPhotograph } from '../../../Svg'

const Container = styled(Flex)`
  align-items: center;
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  height: 400px;
  justify-content: center;
  overflow: hidden;
  padding: 16px;
  width: 400px;

  ${({ theme }) => theme.mediaQueries.sm} {
    height: 500px;
    width: 500px;
  }
`

const StyledError = styled(Flex)`
  align-items: center;
  flex-direction: column;
  justify-content: center;
`

const File = ({ error, isLoading, image }) => {
  return (
    <Container>
      {error !== undefined ? (
        <StyledError>
          <Text>Oops!</Text>
          <Text>Something went wrong.</Text>
        </StyledError>
      ) : isLoading ? (
        <SvgPhotograph height="60px" width="60px" />
      ) : (
        <img src={image} alt="icons" />
      )}
    </Container>
  )
}

export default File
