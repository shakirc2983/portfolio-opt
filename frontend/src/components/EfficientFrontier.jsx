import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

function EfficientFrontier({ result }) {
  const [xData, setXData] = useState([]);
  const [yData, setYData] = useState([]);
  const [sharpeData, setSharpeData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const rangeFrom1ToMax = (max) => {
    return Array.from({ length: max }, (_, i) => i + 1);
  }

  useEffect(() => {
    if (!result) return;

    console.log("EfficientFrontier received result:", result);

    setLoading(true);
    setError(null);

    fetch("/ef")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        console.log("Fetched /ef:", data);
        setXData(data.x || []);
        setYData(data.y || []);
        setSharpeData(data.sharpe || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to fetch /ef:', err);
        setError(err.message);
        setLoading(false);
      });
  }, [result]);

  if (loading) return <p>Loading Efficient Frontier...</p>;
  if (error) return <p>Error loading plot: {error}</p>;

  return (
    <Plot
      data={[
        {
          x: xData,
          y: yData,
          mode: "markers",
          type: "scatter",
          text: rangeFrom1ToMax(result.simulations).map(String),

          marker: {
            size:10,
            color:sharpeData,
            colorscale: "Portland",
            colorbar: {
              title: {text:"Sharpe Ratio"}
            },
            showscale: true,
          }
        },
      ]}
      layout={{
        title: { text: "Efficient Frontier" },
        xaxis: {
          title: { text: "Volatility" },
          showline: true,
          zeroline: false,
        },
        yaxis: {
          title: { text: "Return" },
        },
        width: 600,
        height: 500,
      }}
    />
  );
}

export default EfficientFrontier;
