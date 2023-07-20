import React, { useEffect, useState } from 'react';
import CanvasJSReact from '@canvasjs/react-charts';

var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

const App = ({ selectedJobTitle }) => {
  const [dataPoints, setDataPoints] = useState([]);
  useEffect(() => {
    fetchData();
  }, [selectedJobTitle]);
  const addSymbols = (e) => {
    var suffixes = ['', 'K', 'M', 'B'];
    var order = Math.max(Math.floor(Math.log(Math.abs(e.value)) / Math.log(1000)), 0);
    if (order > suffixes.length - 1) order = suffixes.length - 1;
    var suffix = suffixes[order];
    return CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
  };

  const fetchData = () => {
   fetch(`http://localhost:3001/api/analysis/${selectedJobTitle}`)
     .then((response) => response.json())
     .then((data) => {
       const transformedData = data.map((item, index) => {
         return { label: item[0], y: parseInt(item[1]) };
       });
       setDataPoints(transformedData);
     })
     .catch((error) => {
       console.error('Error fetching data:', error);
     });
 };
 

  const options = {
    animationEnabled: true,
    theme: 'light2',
    title: {
      text: `${selectedJobTitle}`,
    },
    axisX: {
      title: 'Skills',
      reversed: true,
    },
    axisY: {
      title: 'Current Demand',
      includeZero: true,
      labelFormatter: addSymbols,
    },
    data: [
      {
        type: 'bar',
        dataPoints: dataPoints,
      },
    ],
  };
  return (
    <div>
      <CanvasJSChart options={options} />
    </div>
  );
};

export default App;
