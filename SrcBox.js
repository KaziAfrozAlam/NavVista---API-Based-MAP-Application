// Perform a search for the entered location
function performSearch() {
  // Get the user input from the search input field
  var userInput = document.getElementById('search-input').value;

  // Create a new PlacesService instance
  var placesService = new google.maps.places.PlacesService(map);

  // Create a request object for the Places API search
  var request = {
    query: userInput
  };

  // Perform the search request
  placesService.textSearch(request, function(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK && results && results.length > 0) {
      // Extract the first result
      var firstResult = results[0];

      // Get the location and viewport bounds of the result
      var location = firstResult.geometry.location;
      var viewport = firstResult.geometry.viewport;

      // Update the map to center on the location and fit the viewport bounds
      map.setCenter(location);
      map.fitBounds(viewport);
    } else {
      // Handle the case when no results are found
      console.log('No results found for the search query.');
    }
  });
}
