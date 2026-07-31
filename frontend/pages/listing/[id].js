import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'

export default function ListingPage() {
  const router = useRouter()
  const { id } = router.query
  const [price, setPrice] = useState(null)
  const [messages, setMessages] = useState([])

  useEffect(() => {
    if (!id) return
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${proto}://${window.location.host}/ws/listing/${id}/`)
    ws.onopen = () => {
      console.log('ws open')
    }
    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data)
        if (data.type === 'price.update') {
          setPrice(data.current_price)
          setMessages(m => [...m, `New bid ${data.current_price} by ${data.bidder}`])
        }
      } catch (err) {
        console.error(err)
      }
    }
    ws.onclose = () => console.log('ws closed')
    return () => ws.close()
  }, [id])

  return (
    <div dir="rtl" style={{fontFamily:'sans-serif',padding:20}}>
      <h1>صفحة المزاد #{id}</h1>
      <p>السعر الحالي: {price ?? 'لا مزايدات بعد'}</p>
      <h3>سجل المزايدات</h3>
      <ul>
        {messages.map((m, idx) => <li key={idx}>{m}</li>)}
      </ul>
      <p>ملاحظة: هذه صفحة عرضية بسيطة لعرض البث اللحظي.</p>
    </div>
  )
}
