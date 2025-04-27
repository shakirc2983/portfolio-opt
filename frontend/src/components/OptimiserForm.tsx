import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

export default function OptimiserForm() {

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate());
    console.log(year + month + day)
    return `${year}-${month}-${day}`;
 };

  return (
    <>
      <Form>
        <Form.Group>
          <Form.Label>Number of Simulations</Form.Label>
          <Form.Control type="number"></Form.Control>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasic">
          <Form.Label>Stock Tickers</Form.Label>
          <Form.Control type="text" placeholder="AAPL, MSFT, ..." />
          <Form.Text className="text-muted">
          Please enter the correct stock ticker
          </Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controidId="startDate">
          <Form.Label>Start Date</Form.Label>
          <Form.Control type="date" placeholder="DD/MM/YYYY" max={formatDate(new Date())}></Form.Control>
        </Form.Group>
        <Form.Group className="mb-3" controlId="endDate">
          <Form.Label>End Date</Form.Label>
          <Form.Control type="date" placeholder="DD/MM/YYYY" max={formatDate(new Date())}></Form.Control>
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </>
  );
}


