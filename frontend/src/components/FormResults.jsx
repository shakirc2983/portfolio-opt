import React from 'react';
import { Table, OverlayTrigger, Tooltip } from 'react-bootstrap';

function FormResults({ data }) {
  return (
    <div className="mt-4">
      <h4>Black-Litterman Model Result</h4>
      <p><strong>Expected Return:</strong> {data.expected_return}</p>
      <p><strong>Volatility:</strong> {data.volatility}</p>
      <p><strong>Sharpe Ratio:</strong> {data.sharpe_ratio}</p>
      <h5>Weights</h5>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Weight</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(data.weights).map(([ticker, weight]) => (
            <tr key={ticker}>
              <td>{ticker}</td>
              <td>
                <OverlayTrigger
                  placement="top"
                  overlay={<Tooltip id={`tooltip-${ticker}`}>{weight}</Tooltip>}
                >
                  <span>
                    {weight.toFixed(4)} ({(weight * 100).toFixed(2)}%)
                  </span>
                </OverlayTrigger>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default FormResults;
