import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'

const TRANSLATIONS = {
  ar: { title: 'دفع عبر زايدني', status: 'حالة', noteOpen: 'سيُفتح نافذة جديدة لصفحة الدفع (محاكٍ) إن نجحت العملية.', noteCopy: 'إذا لم تُفتح، انسخ الرابط يدوياً من الاستجابة أو تواصل مع الدعم.', selectLang: 'اللغة' },
  ku: { title: 'پارەدان بە زايدني', status: 'حاڵەت', noteOpen: 'پاپگەیەکی نوێ دەکرێتەوە بۆ پەیجی پارەدان (نمونە).', noteCopy: 'ئەگەر نەکڕا، بەدەستی لینکی وەڵام بنووسە یان پشتیوانی پەیوەندیبکە.', selectLang: 'زمان' },
  en: { title: 'Pay with Zayidni', status: 'Status', noteOpen: 'A new window will open the sandbox payment page if successful.', noteCopy: 'If it does not open, copy the URL from the response or contact support.', selectLang: 'Language' }
}

export default function PaymentPage(){
  const router = useRouter()
  const { tx } = router.query
  const [status, setStatus] = useState('idle')
  const [lang, setLang] = useState('ar')

  useEffect(()=>{
    const saved = localStorage.getItem('lang')
    if (saved) setLang(saved)
  },[])
  useEffect(()=> localStorage.setItem('lang', lang), [lang])

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

  const t = TRANSLATIONS[lang] || TRANSLATIONS.ar

  return (
    <div dir={lang==='en' ? 'ltr' : 'rtl'} style={{fontFamily:'sans-serif',padding:20}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <h1 style={{margin:0}}>{t.title}</h1>
        <div>
          <label style={{marginRight:8}}>{t.selectLang}:</label>
          <select value={lang} onChange={e=>setLang(e.target.value)}>
            <option value="ar">العربية</option>
            <option value="ku">کوردی</option>
            <option value="en">English</option>
          </select>
        </div>
      </div>
      <p>{t.status}: {status}</p>
      <p>{t.noteOpen}</p>
      <p>{t.noteCopy}</p>
    </div>
  )
}
