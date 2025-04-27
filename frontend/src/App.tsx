import { useState, useEffect } from 'react'
import './App.css'
import OptimiserForm from './components/OptimiserForm.tsx'
import 'bootstrap/dist/css/bootstrap.min.css';
export default function App() {

  // const [data, setData] = useState([{}])
 
  useEffect(() => {
  fetch("/mcs")
    .then(res => res.json())
    .then(data => {
      console.log(data);
    })
    .catch(err => console.error("Fetch error:", err));
}, []);
  return (
    <>
      <div>
        <h1>Monte Carlo Simulation</h1>
        <OptimiserForm/>
      </div>

    </>
  )
}


