import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import Table from 'react-bootstrap/Table';

function Allocation({ result, portfolioData }) {
  const [loading, setLoading] = useState(false);

  const rangeFrom1ToMax = (max) => {
    return Array.from({ length: max }, (_, i) => i + 1);
  }

  return (
    portfolioData && <>
      <Plot
        data={[
          {
            values: portfolioData.weights,
            labels: portfolioData.tickers,
            mode: "markers",

            type: "pie",
          },
        ]}
        layout={{
          width: 600,
          height: 500,
        }}
    
      />
      <Table>
        <thead>
          <tr>
            <th>Tickers</th>
            <th>Weights</th>
            <th>Expected Returns</th>
            <th>Expected Volatility</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{portfolioData.tickers.join(', ')}</td>
            <td>{portfolioData.weights.join(', ')}</td>
            <td>{portfolioData.returns}</td>
            <td>{portfolioData.volatility}</td>
          </tr>
        </tbody>
      </Table>
    </>
  );
}

export default Allocation;
