import { ThemeProvider } from 'styled-components'
import { GlobalStyle, ResetCss } from '../styles'
import { light } from '../theme'

const App = ({ Component, pageProps }) => {
  return (
    <ThemeProvider theme={light}>
      <ResetCss />
      <GlobalStyle />
      <Component {...pageProps} />
    </ThemeProvider>
  )
}

export default App
