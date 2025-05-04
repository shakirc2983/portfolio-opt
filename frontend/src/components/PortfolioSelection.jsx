import React from 'react';
import PortfolioSelectionForm from './PortfolioSelectionForm.jsx';

export default function PortfolioSelection({ result, onPortfolioData }) {
  console.log(result);
  return (
    <>
      <div>Portfolio Selection</div>
      <PortfolioSelectionForm result={result} onPortfolioData={onPortfolioData}/>
      
    </>

  )
}

