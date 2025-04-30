import { useState, useEffect } from 'react'
import './App.css'
import OptimiserForm from './components/OptimiserForm.jsx'
import FormResults from './components/FormResults.jsx'
import EfficientFrontier from './components/EfficientFrontier.jsx'
import 'bootstrap/dist/css/bootstrap.min.css';
export default function App() {
  const [result, setResult] = useState(null);

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
        <OptimiserForm onResult={(data) => setResult(data)} />
        {result && <FormResults data={result} />}
        {result && <EfficientFrontier result={result}/>}
      </div>

    </>
  )
}


