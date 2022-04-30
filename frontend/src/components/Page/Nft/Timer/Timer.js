import { useEffect, useState } from 'react'

import styled, { useTheme } from 'styled-components'

import { Flex, Text } from '../../../Toolkit'

const Container = styled(Flex)`
  align-items: stretch;
  border-radius: ${({ theme }) => theme.radii.small};
  border: 1px dashed ${({ theme }) => theme.colors.borderAlt};
  height: 142px;
  justify-content: center;
  margin-top: 16px;
  padding: 16px;
  width: 400px;

  ${({ theme }) => theme.mediaQueries.sm} {
    width: 500px;
  }

  ${({ theme }) => theme.mediaQueries.lg} {
    width: 100%;
  }
`

const Item = styled(Flex)`
  align-items: center;
  flex-direction: column;
  justify-content: center;
`

const Label = styled(Text)`
  font-size: 10px;
`

const Value = styled(Text)`
  font-size: 58px;
`

const calculateTimeLeft = (date) => {
  const difference = +date - +new Date()

  let timeLeft = {
    days: '0',
    hours: '00',
    minutes: '00',
    seconds: '00',
  }

  if (difference > 0) {
    const days = Math.floor(difference / 1000 / 60 / 60 / 24)
    const hours = Math.floor((difference / 1000 / 60 / 60) % 24)
    const minutes = Math.floor((difference / 1000 / 60) % 60)
    const seconds = Math.floor((difference / 1000) % 60)

    timeLeft.days = timeLeft = {
      days: days.toString(),
      hours: hours <= 9 ? `0${hours.toString()}` : hours.toString(),
      minutes: minutes <= 9 ? `0${minutes.toString()}` : minutes.toString(),
      seconds: seconds <= 9 ? `0${seconds.toString()}` : seconds.toString(),
    }
  }

  return timeLeft
}

const Timer = ({ endDate }) => {
  const theme = useTheme()

  const [timeLeft, setTimeLeft] = useState({
    days: '0',
    hours: '00',
    minutes: '00',
    seconds: '00',
  })

  useEffect(() => {
    const id = setTimeout(() => setTimeLeft(calculateTimeLeft(endDate)), 1000)

    return () => clearTimeout(id)
  })

  const semicolon = (
    <Text fontSize="58px" marginX="10px">
      :
    </Text>
  )

  return (
    <Container>
      <Item>
        <Value>{timeLeft.days}</Value>
        <Label>DAYS</Label>
      </Item>
      {semicolon}
      <Item>
        <Value>{timeLeft.hours}</Value>
        <Label>HOURS</Label>
      </Item>
      {semicolon}
      <Item>
        <Value>{timeLeft.minutes}</Value>
        <Label>MINUTES</Label>
      </Item>
      {semicolon}
      <Item>
        <Value color={theme.colors.action}>{timeLeft.seconds}</Value>
        <Label>SECONDS</Label>
      </Item>
    </Container>
  )
}

export default Timer
