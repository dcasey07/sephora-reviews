// Hosting on AWS S3

const url = "https://sephora-reviews-data-vis.s3.us-east-2.amazonaws.com/oneyear_df.json";
var data_1;

d3.json(url)
  .then(function(data) {
    console.log(data);
    data_1 = data;
  })
  .catch(function(error) {
    console.error("Error retrieving JSON data:", error);
    // Remember to build all of the visualizations within this d3.json structure
    
  });
