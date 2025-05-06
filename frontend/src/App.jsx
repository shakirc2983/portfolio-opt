import { useState, useEffect } from 'react';
import './App.css';
import MCSForm from './components/MCSForm.jsx';
import BLForm from './components/BLForm.jsx';
import FormResults from './components/FormResults.jsx';
import EfficientFrontier from './components/EfficientFrontier.jsx';
import PortfolioSelection from './components/PortfolioSelection.jsx';
import Allocation from './components/Allocation.jsx';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function App() {
  const [result, setResult] = useState(null);
  const [portfolioData, setPortfolioData] = useState(null);
  const [mode, setMode] = useState('mcs'); // "mcs" or "bl"

  useEffect(() => {
    fetch("/mcs")
      .then(res => res.json())
      .then(data => {
        console.log(data);
      })
      .catch(err => console.error("Fetch error:", err));
  }, []);

  return (
    <div className="container mt-4">
      <h1 className="mb-3">
        {mode === "mcs" ? "Monte Carlo Simulation" : "Black-Litterman Model"}
      </h1>

      {/* Toggle Buttons */}
      <div className="mb-4">
        <button
          className={`btn ${mode === "mcs" ? "btn-primary" : "btn-outline-primary"} me-2`}
          onClick={() => {
            setMode("mcs");
            setResult(null);
            setPortfolioData(null);
          }}
        >
          Monte Carlo
        </button>
        <button
          className={`btn ${mode === "bl" ? "btn-primary" : "btn-outline-primary"}`}
          onClick={() => {
            setMode("bl");
            setResult(null);
            setPortfolioData(null);
          }}
        >
          Black-Litterman
        </button>
      </div>

      {/* Conditional Rendering */}
      {mode === "mcs" && (
        <>
          <MCSForm onResult={(data) => setResult(data)} />
          {result && <FormResults data={result} />}
          {result && <EfficientFrontier result={result} />}
          {result && (
            <PortfolioSelection
              result={result}
              onPortfolioData={(data) => setPortfolioData(data)}
            />
          )}
          {portfolioData && (
    <Allocation result={result} portfolioData={portfolioData} />
          )}
        </>
      )}

      {mode === "bl" && (
        <>
          <BLForm onResult={(data) => setResult(data)} />
          {result && <FormResults data={result} />}
        </>
      )}
    </div>
  );
}

