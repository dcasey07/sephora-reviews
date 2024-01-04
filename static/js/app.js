const url = "https://sephora-reviews-data-vis.s3.us-east-2.amazonaws.com/oneyear_df.json";

// Set variable to make console.logs outside of d3 call
var data_1;

d3.json(url)
  .then(function(data) {
    console.log(data);

    // Copy data to variable set outside of d3 call 
    data_1 = data;

    // Extract unique secondary categories
    var secondaryCategories = Array.from(new Set(data.map(item => item.secondary_category)));
    // Extract unique brand names
    var brandNames = Array.from(new Set(data.map(item => item.brand_name)));

    // Populate the category dropdown menu with 'All' option
    var dropdownCatMenu = d3.select("#selDatasetCat");
    dropdownCatMenu.append("option").text("All").property("value", "");
    secondaryCategories.forEach(function(category) {
      dropdownCatMenu.append("option").text(category).property("value", category);
    });

    // Populate the brand dropdown menu with 'All' option
    var dropdownBrandMenu = d3.select("#selDatasetBrand");
    dropdownBrandMenu.append("option").text("All").property("value", "");
    brandNames.forEach(function(brand) {
      dropdownBrandMenu.append("option").text(brand).property("value", brand);
    });

    // Function to update the page content for categories
    function updateContentByCategory(selectedCategory) {
      var filteredCategory = selectedCategory === "" ? data : data.filter(item => item.secondary_category === selectedCategory);
      // Update graphs for category
      // updateGraphByCategory(filteredCategory);
    }

    // Function to update the page content for brands
    function updateContentByBrand(selectedBrand) {
      var filteredBrand = selectedBrand === "" ? data : data.filter(item => item.brand_name === selectedBrand);
      // Update graphs for brand
      // updateGraphByBrand(filteredBrand);
    }

    // Add event listener to the category dropdown menu
    dropdownCatMenu.on("change", function() {
      var selectedCategory = d3.select(this).property("value");
      updateContentByCategory(selectedCategory);
    });

    // Add event listener to the brand dropdown menu
    dropdownBrandMenu.on("change", function() {
      var selectedBrand = d3.select(this).property("value");
      updateContentByBrand(selectedBrand);
    });

    // Initial update with 'All' categories and 'All' brands
    updateContentByCategory("");
    updateContentByBrand("");
  })
  .catch(function(error) {
    console.error("Error retrieving JSON data:", error);
  });
