// Uncomment the url out if you need to test with the complete json, and use "url" to call d3.json

// const url = "https://sephora-reviews-data-vis.s3.us-east-2.amazonaws.com/oneyear_df.json";

// Route APIs
const catBrandDropdownURL = "http://127.0.0.1:5000/api/v1.0/catbranddropdown";
const valueScoreURL = 'http://127.0.0.1:5000/api/v1.0/valuescore';
const ratingPriceCorr = 'http://127.0.0.1:5000/api/v1.0/rating_vs_price';

// Call to populate dropdowns and update on load
d3.json(catBrandDropdownURL).then(data => {
    populateDropdown("#selDatasetCat", data.categories);
    populateDropdown("#selDatasetBrand", data.brands);
    d3.select("#selDatasetCat").on("change", updateCharts);
    d3.select("#selDatasetBrand").on("change", updateCharts);
    updateCharts();
}).catch(error => console.error('Error fetching dropdown data:', error));

function populateDropdown(selector, options) {
    var dropdownMenu = d3.select(selector);
    dropdownMenu.append("option").text("All").property("value", "");
    options.forEach(option => dropdownMenu.append("option").text(option).property("value", option));
}

function updateCharts() {
  var selectedCategory = d3.select("#selDatasetCat").property("value");
  var selectedBrand = d3.select("#selDatasetBrand").property("value");
  updateBarChart(selectedCategory, selectedBrand);
  updateScatterPlot(selectedCategory, selectedBrand);
  displayTopTenValuescore(selectedCategory, selectedBrand);
}

// Encode the URL so it can pass non-alphanumeric characters
function buildQueryURL(baseUrl, category, brand) {
    return `${baseUrl}?secondary_category=${encodeURIComponent(category)}&brand_name=${encodeURIComponent(brand)}`;
}

function updateBarChart(category, brand) {
    var queryUrl = buildQueryURL(valueScoreURL, category, brand);
    d3.json(queryUrl).then(createBarChart).catch(error => console.error('Error:', error));
}

function updateScatterPlot(category, brand) {
    var queryUrl = buildQueryURL(ratingPriceCorr, category, brand);
    d3.json(queryUrl).then(createScatterPlot).catch(error => console.error('Error:', error));
}

function createBarChart(data) {
    const top10Data = data.sort((a, b) => b.value_score - a.value_score).slice(0, 10);
    const productNames = top10Data.map(item => item.product_name);
    const valueScores = top10Data.map(item => item.value_score);
    const plotData = [{ x: productNames, y: valueScores, type: 'bar' }];
    const layout = { title: 'Top 10 Products by Normalized Value Score', xaxis: { title: 'Product Name' }, yaxis: { title: 'Normalized Value Score' } };
    Plotly.newPlot('barChart', plotData, layout);
}

function createScatterPlot(data) {
    const prices = data.map(item => item.price_usd);
    const ratings = data.map(item => item.average_rating);
    const hoverTexts = data.map(item => `Product: ${item.product_name}<br>Brand: ${item.brand_name}<br>Price: $${item.price_usd.toFixed(2)}<br>Average Rating: ${item.average_rating.toFixed(2)}<br>Review Count: ${item.review_count}`);
    const plotData = [{ x: prices, y: ratings, mode: 'markers', type: 'scatter', text: hoverTexts, hoverinfo: 'text', marker: { size: 10 } }];
    const layout = { title: 'Average Rating vs Price', xaxis: { title: 'Price (USD)' }, yaxis: { title: 'Average Rating' }, hovermode: 'closest' };
    Plotly.newPlot('scatter', plotData, layout);
}

function displayTopTenValuescore(category, brand) {
  var queryUrl = buildQueryURL(valueScoreURL, category, brand);
  d3.json(queryUrl).then(data => {
      const topTenProducts = data.sort((a, b) => b.value_score - a.value_score).slice(0, 10);
      const panelBody = d3.select("#valuescore");
      panelBody.html("");

      const ol = panelBody.append("ol").classed("list-group", true);

      topTenProducts.forEach((product, index) => {
          ol.append("li")
            .classed("list-group-item", true)
            .html(`<strong>${index + 1}) ${product.product_name}</strong> (${product.brand_name}) - $${product.price_usd.toFixed(2)} | Avg Rating: ${product.average_rating.toFixed(2)}, Reviews: ${product.review_count}`)
            .attr("title", `Value Score: ${product.value_score.toFixed(2)}`);
      });
  }).catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function() {
  const panelTitle = d3.select("#panelTitle");
  panelTitle.attr("title", "Value Score is a measure of product quality, popularity, and affordability. It is calculated based on average customer ratings, the number of reviews, and the product price, ensuring that higher scores represent better overall value relative to the product's listing price. Value Score is purely for research purposes and is in no way intended as a product advertisement or indication of guaranteed success when purchasing products.");

  displayTopTenValuescore(); 
});