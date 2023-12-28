// Hosting on AWS S3

const url = "https://sephora-reviews-data-vis.s3.us-east-2.amazonaws.com/complete_json.json";

var data_1;

d3.json(url)
  .then(function(data) {
    console.log(data);
    const limitedData = data.slice(0, 5);
    console.log(limitedData);
    data_1 = data;
  })
  .catch(function(error) {
    console.error("Error retrieving JSON data:", error);
  });

// Local Fetching

//   const jsonFilePath = '../../Resources/complete_json.json';
//   const cors = require('cors');
//   app.use(cors());
  
//   fetch(jsonFilePath)
//       .then(response => {
//           if (!response.ok) {
//               throw new Error('Network response was not ok ' + response.statusText);
//           }
//           return response.json();
//       })
//       .then(data => {
//           console.log(data);
//       })
//       .catch(error => {
//           console.error('Error retrieving JSON data:', error);
//       });


