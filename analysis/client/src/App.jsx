import React, { useState } from 'react';
import BarChart from './BarChart';
import './App.css';

function App() {
  const [selectedJobTitle, setSelectedJobTitle] = useState('');

  const handleJobTitleChange = (event) => {
    setSelectedJobTitle(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Skills Analysis</h1>
        <select value={selectedJobTitle} onChange={handleJobTitleChange} className='menu'>
          <option value="Data_analyst">Data Analyst</option>
          <option value="Data_engineer">Data Engineer</option>
          <option value="Data_scientist">Data Scientist</option>
          <option value="Business_analyst">Business Analyst</option>
          <option value="Cloud_engineer">Cloud Engineer</option>
          <option value="Software_engineer">Software Engineer</option>
        </select>
          {selectedJobTitle && <BarChart selectedJobTitle={selectedJobTitle} />}
      </header>
    </div>
  );
}

export default App;
