import React from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

export default function PortfolioSelectionForm({simulations}) {
  const [validated, setValidated] = useState(false);
  const [errors, setErrors] = useState({
    simulations: false
  });

  const getPortfolio = (id) => {
    return;

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
      getPortfolio(element["simulations"])
    }
  };

  return (
    <>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="portfolio-id">
          <Form.Label>Portfolio ID</Form.Label>
          <Form.Control type="number" min="1" max={String(simulations)} isInvalid={errors.simulations}></Form.Control>
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </>
  )
}

