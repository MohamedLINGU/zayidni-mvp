import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'

export default function ListingPage() {
  const router = useRouter()
  const { id } = router.query
  const [price, setPrice] = useState(null)
  const [messages, setMessages] = useState([])
  const [pending, setPending] = useState(null)

  useEffect(() => {
    if (!id) return

    // WebSocket for live updates
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

    // Check for pending transaction for the current logged-in user
    (async () => {
      try {
        const res = await fetch(`/api/payments/pending_for_listing/?listing_id=${id}`)
        if (res.ok) {
          const data = await res.json()
          setPending(data)
        }
      } catch (e) {
        console.warn('could not load pending tx', e)
      }
    })()

    return () => ws.close()
  }, [id])

  return (
    <div dir="rtl" style={{fontFamily:'sans-serif',padding:20}}>
      <h1>صفحة المزاد #{id}</h1>
      <p>السعر الحالي: {price ?? 'لا مزايدات بعد'}</p>

      {pending && pending.found ? (
        <div style={{margin:'12px 0', padding:10, border:'1px solid #ddd', borderRadius:6}}>
          <button onClick={() => window.open(`/payment/${pending.transaction_id}`, '_blank')} style={{padding:'10px 16px',background:'#0b69ff',color:'#fff',border:'none',borderRadius:6}}>ادفع الآن</button>
          <p style={{marginTop:8}}>حالة المعاملة: {pending.status}</p>
        </div>
      ) : null}

      <h3>سجل المزايدات</h3>
      <ul>
        {messages.map((m, idx) => <li key={idx}>{m}</li>)}
      </ul>
      <p>ملاحظة: هذه صفحة عرضية بسيطة لعرض البث اللحظي.</p>
    </div>
  )
}
