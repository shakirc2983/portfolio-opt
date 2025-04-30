import React from "react";

function FormResults({ data }) {
  return (
    <div>
      <h3>Simulation Results</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default FormResults;
