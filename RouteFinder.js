// Define global variables
var directionsService;
var directionsRenderer;
var directionsResultContainer;

// Initialize and load the map
function initMap() {
  // Existing code...

  // Initialize DirectionsService and DirectionsRenderer
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);
  
  // Get directions result container
  directionsResultContainer = document.getElementById("directions-result");

  // Add event listener to the directions form submission
  document.getElementById("directions-form").addEventListener("submit", calculateDirections);
}

// Calculate and display directions
function calculateDirections(event) {
  event.preventDefault(); // Prevent form submission

  // Get the origin and destination input values
  var originInput = document.getElementById("origin-input").value;
  var destinationInput = document.getElementById("destination-input").value;

  // Create a request object for the Directions API
  var request = {
    origin: originInput,
    destination: destinationInput,
    travelMode: google.maps.TravelMode.DRIVING // Adjust travel mode as needed
  };

  // Call the DirectionsService to calculate the directions
  directionsService.route(request, function(result, status) {
    if (status === google.maps.DirectionsStatus.OK) {
      // Display the directions on the map using the DirectionsRenderer
      directionsRenderer.setDirections(result);
      directionsRenderer.setPanel(directionsResultContainer);
    } else {
      // Handle the case when no directions are found
      directionsResultContainer.innerHTML = "No directions found.";
    }
  });
}
