import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import {useState, useRef} from 'react';

import APIService from '../components/APIService.jsx';

export default function OptimiserForm({ onResult }) {
  const [validated, setValidated] = useState(false);
  const submitButtonRef = useRef(null);

  const [errors, setErrors] = useState({
    simulations: false,
    tickers: false,
    startDate: false,
    endDate: false,
  });

  const [data, setData] = useState([]);

  const formatDate = (date) => {
    const yesterday = new Date(date)
    yesterday.setDate(yesterday.getDate() - 1)
    return yesterday.toISOString().split("T")[0];
 };
 const runMCS = (data) => {

    const existingErrorBox = document.querySelector('.alert-danger');

    if (submitButtonRef.current) {
      submitButtonRef.current.disabled = true;
    }

    if (existingErrorBox) {
      existingErrorBox.remove();
    }

    APIService.RunMCS(data)
    .then((response) => {
      //console.log(response)
      if(response.error) {
          const errorBox = document.createElement('div');
          errorBox.className = 'alert alert-danger';
          errorBox.setAttribute('role', 'alert');
          errorBox.innerText = `Error: ${response.error}`;
          document.body.appendChild(errorBox);      }
      if (response.data) {
          onResult(response.data);
      }
    })
    .catch(error => console.log('error',error))
    .finally(() => {
        if (submitButtonRef.current) {
          submitButtonRef.current.disabled = false;
        }
      });
  }

  const checkValid = (element) => {
    return element == false;
  }

 const handleSubmit = (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    const updatedErrors = { ...errors };
    const elementArray = Array.from(e.currentTarget.elements);
    const data = [];

    elementArray.map(function(element) {
      if (element instanceof HTMLInputElement) {
        updatedErrors[element.id] = element.value.trim() === '';
        data.push(element.value);
      }
    });

    setErrors(updatedErrors);

    if (Object.values(updatedErrors).every(checkValid)) {
      setData(data);
      runMCS(data);
    }


  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="simulations">
          <Form.Label>Number of Simulations</Form.Label>
          <Form.Control type="number" isInvalid={errors.simulations} min="1"></Form.Control>
        </Form.Group>
        <Form.Group className="mb-3" controlId="tickers">
          <Form.Label>Stock Tickers</Form.Label>
          <Form.Control type="text" placeholder="AAPL, MSFT, ..." isInvalid={errors.tickers}/>
          <Form.Text className="text-muted">
          Please enter the correct stock ticker
          </Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="startDate">
          <Form.Label>Start Date</Form.Label>
          <Form.Control type="date" placeholder="DD/MM/YYYY" max={formatDate(new Date())} isInvalid={errors.startDate}></Form.Control>
        </Form.Group>
        <Form.Group className="mb-3" controlId="endDate">
          <Form.Label>End Date</Form.Label>
          <Form.Control type="date" placeholder="DD/MM/YYYY" max={formatDate(new Date())} isInvalid={errors.endDate}></Form.Control>
        </Form.Group>
        <Button variant="primary" type="submit" ref={submitButtonRef}>
          Submit
        </Button>
      </Form>
    </>
  );
}
