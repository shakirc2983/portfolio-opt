import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import { useState, useRef } from 'react';
import APIService from '../components/APIService.jsx';

export default function BLForm({ onResult }) {
  const submitButtonRef = useRef(null);

  const [views, setViews] = useState([{ ticker: "", expectedReturn: "", confidence: 0.5 }]);
  const [errors, setErrors] = useState({
    tickers: false,
    startDate: false,
    endDate: false,
  });

  const [data, setData] = useState([]);

  const formatDate = (date) => {
    const yesterday = new Date(date);
    yesterday.setDate(yesterday.getDate() - 1);
    return yesterday.toISOString().split("T")[0];
  };

  const buildBLPayload = () => {
    const viewDict = {};
    const confidenceDict = {};

    views.forEach(({ ticker, expectedReturn, confidence }) => {
      if (ticker && expectedReturn) {
        viewDict[ticker.trim()] = parseFloat(expectedReturn);
        confidenceDict[ticker.trim()] = parseFloat(confidence);
      }
    });

    return {
      tickers: document.getElementById("tickers").value.trim(),
      start_date: document.getElementById("startDate").value,
      end_date: document.getElementById("endDate").value,
      views: viewDict,
      confidences: confidenceDict,
    };
  };

  const runBL = () => {
    const existingErrorBox = document.querySelector('.alert-danger');
    if (submitButtonRef.current) submitButtonRef.current.disabled = true;
    if (existingErrorBox) existingErrorBox.remove();

    const data = buildBLPayload();

    APIService.RunBL(data)
      .then((response) => {
        if (response.error) {
          const errorBox = document.createElement('div');
          errorBox.className = 'alert alert-danger';
          errorBox.setAttribute('role', 'alert');
          errorBox.innerText = `Error: ${response.error}`;
          submitButtonRef.current.insertAdjacentElement('afterend', errorBox);
        }
        if (response.data) {
          onResult(response.data);
        }
      })
      .catch(error => console.log('error', error))
      .finally(() => {
        if (submitButtonRef.current) submitButtonRef.current.disabled = false;
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    const updatedErrors = { ...errors };

    const tickersRaw = form.elements.tickers.value;
    const tickersArray = tickersRaw.split(',').map(t => t.trim()).filter(Boolean);

    const startDate = form.elements.startDate.value;
    const endDate = form.elements.endDate.value;

    updatedErrors.tickers = tickersArray.length === 0;
    updatedErrors.startDate = startDate === '';
    updatedErrors.endDate = endDate === '';

    setErrors(updatedErrors);

    if (Object.values(updatedErrors).every(val => !val)) {
      const payload = {
        tickers: tickersArray,
        startDate,
        endDate,
        views
      };
      setData(payload);
      runBL(payload);
    }
  };


  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="tickers">
          <Form.Label>Stock Tickers</Form.Label>
          <Form.Text className="text-muted">
            <div>Please enter the correct stock ticker</div>
          </Form.Text>
          <Form.Control type="text" placeholder="AAPL, MSFT, ..." isInvalid={errors.tickers} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="startDate">
          <Form.Label>Start Date</Form.Label>
          <Form.Text className="text-muted">
            <div>Gap between both dates must be 2 days or more</div>
          </Form.Text>
          <Form.Control type="date" max={formatDate(new Date())} isInvalid={errors.startDate} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="endDate">
          <Form.Label>End Date</Form.Label>
          <Form.Control type="date" max={formatDate(new Date())} isInvalid={errors.endDate} />
        </Form.Group>

        <Form.Label>Views and Confidences</Form.Label>
        {views.map((view, index) => (
          <div key={index} className="mb-3 d-flex gap-2 align-items-center">
            <Form.Control
              type="text"
              placeholder="Ticker (e.g., AAPL)"
              value={view.ticker}
              onChange={(e) => {
                const newViews = [...views];
                newViews[index].ticker = e.target.value;
                setViews(newViews);
              }}
            />
            <Form.Control
              type="number"
              placeholder="Expected Return (e.g., 0.05)"
              step="0.01"
              value={view.expectedReturn}
              onChange={(e) => {
                const newViews = [...views];
                newViews[index].expectedReturn = e.target.value;
                setViews(newViews);
              }}
            />
            <Form.Control
              type="number"
              placeholder="Confidence (0–1)"
              step="0.1"
              min="0"
              max="1"
              value={view.confidence}
              onChange={(e) => {
                const newViews = [...views];
                newViews[index].confidence = e.target.value;
                setViews(newViews);
              }}
            />
            <Button variant="danger" onClick={() => {
              const newViews = views.filter((_, i) => i !== index);
              setViews(newViews);
            }}>✕</Button>
          </div>
        ))}

        <Button
          variant="secondary"
          className="mb-3"
          onClick={() => setViews([...views, { ticker: "", expectedReturn: "", confidence: 0.5 }])}
        >
          + Add View
        </Button>

        <br />
        <Button variant="primary" type="submit" ref={submitButtonRef}>
          Run Optimiser
        </Button>
      </Form>
    </>
  );
}

