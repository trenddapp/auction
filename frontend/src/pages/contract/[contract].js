import { useRouter } from 'next/router'
import { useEffect } from 'react'

const Contract = () => {
  const router = useRouter()
  const { contract } = router.query

  useEffect(() => {
    // TODO: Fetch contract nfts.
    console.log(contract)
  }, [])

  return <div>Contract Page</div>
}

export default Contract
