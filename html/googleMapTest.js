function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: {lat: -34.397, lng: 150.644} // This will be replaced by the actual coordinates
    });
  
    // Geocoding the address
    var geocoder = new google.maps.Geocoder();
    geocodeAddress(geocoder, map);
  }
  
  function geocodeAddress(geocoder, resultsMap) {
    var address = "〒105-0011 東京都港区芝公園４丁目２−８"; 
    geocoder.geocode({'address': address}, function(results, status) {
      if (status === 'OK') {
        resultsMap.setCenter(results[0].geometry.location);
        new google.maps.Marker({
          map: resultsMap,
          position: results[0].geometry.location,
          icon: './googleMapTestPin.png' // Path to your custom image
        });
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
  }
  
  window.initMap = initMap;
  