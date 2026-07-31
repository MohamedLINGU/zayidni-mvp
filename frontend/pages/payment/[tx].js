import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'

export default function PaymentPage(){
  const router = useRouter()
  const { tx } = router.query
  const [status, setStatus] = useState('idle')
  useEffect(() => {
    if (!tx) return
    const doCreate = async () => {
      setStatus('creating')
      try {
        const res = await fetch(`/api/payments/create_session/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ transaction_id: tx })
        })
        const data = await res.json()
        if (res.ok && data.payment_url) {
          setStatus('redirecting')
          window.open(data.payment_url, '_blank')
        } else {
          setStatus('error')
          console.error(data)
        }
      } catch (err) {
        setStatus('error')
        console.error(err)
      }
    }
    doCreate()
  }, [tx])

  return (
    <div dir="rtl" style={{fontFamily:'sans-serif',padding:20}}>
      <h1>دفع عبر زايدني</h1>
      <p>حالة: {status}</p>
      <p>سيُفتح نافذة جديدة لصفحة الدفع (محاكٍ) إن نجحت العملية.</p>
      <p>إذا لم تُفتح، انسخ الرابط يدوياً من الاستجابة أو تواصل مع الدعم.</p>
    </div>
  )
}
