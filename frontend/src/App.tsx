import { useState, useEffect } from 'react'
import './App.css'

export default function App() {

  const [data, setData] = useState([{}])
 
  useEffect(() => {
  fetch("/mcs")
    .then(res => res.json())
    .then(text => {
      console.log("Raw response:");
      console.log(text);
    })
    .catch(err => console.error("Fetch error:", err));
}, []);
  return (
    <>
      <div>

      </div>

    </>
  )
}


