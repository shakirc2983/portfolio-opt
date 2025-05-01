import React from 'react';
import PortfolioSelectionForm from './PortfolioSelectionForm.jsx';

export default function PortfolioSelection({ result }) {
  return (
    <>
      <div>Portfolio Selection</div>
      <PortfolioSelectionForm simulations={result["simulations"]}/>
    </>

  )
}

