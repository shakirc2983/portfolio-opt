import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import {useState} from 'react';

import APIService from '../components/APIService.tsx';

export default function OptimiserForm() {
  const [validated, setValidated] = useState(false);

  const [errors, setErrors] = useState({
    simulations: false,
    tickers: false,
    startDate: false,
    endDate: false,
  });

  const [data, setData] = useState([]);

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate() - 1);
    console.log(year + month + day)
    return `${year}-${month}-${day}`;
 };
 const runMCS = (data) => {
    APIService.RunMCS(data)
    .then((response) => console.log('Success', response))
    .catch(error => console.log('error',error))
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
          <Form.Control type="number" isInvalid={errors.simulations}></Form.Control>
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
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </>
  );
}
