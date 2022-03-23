import dynamic from 'next/dynamic'
import { ThemeProvider } from 'styled-components'
import { GlobalStyle, ResetCss } from '../styles'
import { light } from '../theme'

// TODO: Remove dynamic import when web3-react supports ssr.
const ToastsContainer = dynamic(
  () => {
    return import('../components/Toast').then((module) => {
      return module.ToastContainer
    })
  },
  { ssr: false },
)

// TODO: Remove dynamic import when web3-react supports ssr.
const ToastsProvider = dynamic(
  () => {
    return import('../store/Toasts').then((module) => {
      return module.ToastsProvider
    })
  },
  { ssr: false },
)

const App = ({ Component, pageProps }) => {
  return (
    <ThemeProvider theme={light}>
      <ToastsProvider>
        <ResetCss />
        <GlobalStyle />
        <ToastsContainer />
        <Component {...pageProps} />
      </ToastsProvider>
    </ThemeProvider>
  )
}

export default App
