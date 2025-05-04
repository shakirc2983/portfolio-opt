import React from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import {useState, useEffect} from 'react';

export default function PortfolioSelectionForm({result, onPortfolioData}) {
  const [validated, setValidated] = useState(false);
  const [errors, setErrors] = useState({
    simulations: false
  });

  const checkValid = (element) => {
    return element == false;
  }

  console.log(result);

  const getPortfolio = (id) => {
  fetch(`/portfolio/${id}`)
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((data) => {
      console.log('Fetched portfolio data:', data);

      onPortfolioData(data);
      // Optionally set state here
      // setPortfolio(data);
    })
    .catch((err) => {
      console.error('Failed to fetch /portfolio:', err);
    });
};

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
      console.log(data[0]);
      getPortfolio(data[0]);
    }
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="portfolio-id">
          <Form.Label>Portfolio ID</Form.Label>
          <Form.Control type="number" min="1" max={String(result.simulations)} isInvalid={errors.simulations}></Form.Control>
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </>
  )
}

