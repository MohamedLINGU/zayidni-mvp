import Link from 'next/link'
export default function Home(){
  return (
    <div dir="rtl" style={{fontFamily:'sans-serif',padding:20}}>
      <h1>زايدني — تجربة مزايدة حية (عرض توضيحي)</h1>
      <p>اذهب لصفحة مزاد تجريبي برقم 1</p>
      <Link href="/listing/1">عرض المزاد #1</Link>
    </div>
  )
}
