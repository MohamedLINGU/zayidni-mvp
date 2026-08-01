import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'

const TRANSLATIONS = {
  ar: {
    pageTitle: (id) => `صفحة المزاد #${id}`,
    currentPrice: 'السعر الحالي',
    noBids: 'لا مزايدات بعد',
    bidLog: 'سجل المزايدات',
    note: 'ملاحظة: هذه صفحة عرضية بسيطة لعرض البث اللحظي.',
    payNow: 'ادفع الآن',
    txStatus: 'حالة المعاملة',
    selectLang: 'اللغة',
  },
  ku: {
    pageTitle: (id) => `لاپەڕەی داوەڕی #${id}`,
    currentPrice: 'نرخی ئێستا',
    noBids: 'هیچ داوا نەکراوە',
    bidLog: 'تۆماری داواکان',
    note: 'تێبینی: ئەم لاپەڕەیە نموونەیە بۆ وەشانەی زەندە.',
    payNow: 'ئێستا پارە بدە',
    txStatus: 'بارەی دابەشکردن',
    selectLang: 'زمان',
  },
  en: {
    pageTitle: (id) => `Listing page #${id}`,
    currentPrice: 'Current price',
    noBids: 'No bids yet',
    bidLog: 'Bid history',
    note: 'Note: simple demo page for live broadcast.',
    payNow: 'Pay now',
    txStatus: 'Transaction status',
    selectLang: 'Language',
  }
}

export default function ListingPage() {
  const router = useRouter()
  const { id } = router.query
  const [price, setPrice] = useState(null)
  const [messages, setMessages] = useState([])
  const [pending, setPending] = useState(null)
  const [lang, setLang] = useState('ar')

  useEffect(() => {
    const saved = localStorage.getItem('lang')
    if (saved) setLang(saved)
  }, [])

  useEffect(() => {
    localStorage.setItem('lang', lang)
  }, [lang])

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

  const t = TRANSLATIONS[lang] || TRANSLATIONS.ar
  return (
    <div dir={lang === 'en' ? 'ltr' : 'rtl'} style={{fontFamily:'sans-serif',padding:20}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <h1 style={{margin:0}}>{t.pageTitle(id)}</h1>
        <div>
          <label style={{marginRight:8}}>{t.selectLang}:</label>
          <select value={lang} onChange={e=>setLang(e.target.value)}>
            <option value="ar">العربية</option>
            <option value="ku">کوردی</option>
            <option value="en">English</option>
          </select>
        </div>
      </div>

      <p>{t.currentPrice}: {price ?? t.noBids}</p>

      {pending && pending.found ? (
        <div style={{margin:'12px 0', padding:10, border:'1px solid #ddd', borderRadius:6}}>
          <button onClick={() => window.open(`/payment/${pending.transaction_id}`, '_blank')} style={{padding:'10px 16px',background:'#0b69ff',color:'#fff',border:'none',borderRadius:6}}>{t.payNow}</button>
          <p style={{marginTop:8}}>{t.txStatus}: {pending.status}</p>
        </div>
      ) : null}

      <h3>{t.bidLog}</h3>
      <ul>
        {messages.map((m, idx) => <li key={idx}>{m}</li>)}
      </ul>
      <p>{t.note}</p>
    </div>
  )
}
