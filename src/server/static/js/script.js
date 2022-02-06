// Color markers
var redIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});
var greenIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});
var orangeIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});
var yellowIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

// Initialize map
var map = L.map("map");
var mbAttr =
  '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>';
var mbUrl =
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}";
var grayscale = L.tileLayer(mbUrl, {
  id: "mapbox/light-v10",
  tileSize: 512,
  zoomOffset: -1,
  attribution: mbAttr,
  accessToken:
    "pk.eyJ1IjoicXdlcnRxd2VydCIsImEiOiJja3o5em84aHEwMWFuMnZwZjlyNmRjOG16In0.LQhfH1fxUa4Vds54POk2Xw",
});
var streets = L.tileLayer(mbUrl, {
  id: "mapbox/streets-v11",
  tileSize: 512,
  zoomOffset: -1,
  attribution: mbAttr,
  accessToken:
    "pk.eyJ1IjoicXdlcnRxd2VydCIsImEiOiJja3o5em84aHEwMWFuMnZwZjlyNmRjOG16In0.LQhfH1fxUa4Vds54POk2Xw",
});
grayscale.addTo(map);

// Geolocation
map.locate({ setView: true, maxZoom: 16 });
function onLocationFound(e) {
  var radius = e.accuracy;
  L.marker(e.latlng).addTo(map).bindPopup("You are here").openPopup();
  L.circle(e.latlng, radius).addTo(map);
}
map.on("locationfound", onLocationFound);
function onLocationError(e) {
  alert(e.message);
}
map.on("locationerror", onLocationError);

// Clicking on map and see coordinates
// var popup = L.popup();
// function onMapClick(e) {
//   popup
//     .setLatLng(e.latlng)
//     .setContent("You clicked the map at " + e.latlng.toString())
//     .openOn(map);
// }
// map.on("click", onMapClick);

// Create bin layer groups
var greenBins = L.layerGroup();
var yellowBins = L.layerGroup();
var orangeBins = L.layerGroup();
var redBins = L.layerGroup();

// Fetch bins list, then create corresponding markers, then create the layers controls
fetch("/")
  .then((response) => response.json())
  .then((data) => {
    data.forEach(this.createBinMarkers);
  })
  .then(() => {
    this.createLayersControl();
  });

// Create marker and add to layer group, according to bin fullness
function createBinMarkers(obj, index, array) {
  var fullness = obj.properties.fullness;
  if (fullness <= 40) {
    L.geoJSON(obj, {
      pointToLayer: function (geoJsonPoint, latlng) {
        return L.marker(latlng, { icon: greenIcon });
      },
    })
      .bindPopup(function (layer) {
        return (
          "<h6> Bin ID: " +
          layer.feature.properties.id +
          "</h6><p>Status: " +
          layer.feature.properties.status +
          "</p><p>Updated: " +
          layer.feature.properties.updated +
          "</p><p>Fullness: " +
          layer.feature.properties.fullness +
          "</p>"
        );
      })
      .addTo(greenBins);
  } else if (fullness <= 60) {
    L.geoJSON(obj, {
      pointToLayer: function (geoJsonPoint, latlng) {
        return L.marker(latlng, { icon: yellowIcon });
      },
    })
      .bindPopup(function (layer) {
        return (
          "<h6> Bin ID: " +
          layer.feature.properties.id +
          "</h6><p>Status: " +
          layer.feature.properties.status +
          "</p><p>Updated: " +
          layer.feature.properties.updated +
          "</p><p>Fullness: " +
          layer.feature.properties.fullness +
          "</p>"
        );
      })
      .addTo(yellowBins);
  } else if (fullness <= 80) {
    L.geoJSON(obj, {
      pointToLayer: function (geoJsonPoint, latlng) {
        return L.marker(latlng, { icon: orangeIcon });
      },
    })
      .bindPopup(function (layer) {
        return (
          "<h6> Bin ID: " +
          layer.feature.properties.id +
          "</h6><p>Status: " +
          layer.feature.properties.status +
          "</p><p>Updated: " +
          layer.feature.properties.updated +
          "</p><p>Fullness: " +
          layer.feature.properties.fullness +
          "</p>"
        );
      })
      .addTo(orangeBins);
  } else {
    L.geoJSON(obj, {
      pointToLayer: function (geoJsonPoint, latlng) {
        return L.marker(latlng, { icon: redIcon });
      },
    })
      .bindPopup(function (layer) {
        return (
          "<h6> Bin ID: " +
          layer.feature.properties.id +
          "</h6><p>Status: " +
          layer.feature.properties.status +
          "</p><p>Updated: " +
          layer.feature.properties.updated +
          "</p><p>Fullness: " +
          layer.feature.properties.fullness +
          "</p>"
        );
      })
      .addTo(redBins);
  }
}

// Create the layers control to switch between different base layers and switch overlays
function createLayersControl() {
  greenBins.addTo(map);
  yellowBins.addTo(map);
  orangeBins.addTo(map);
  redBins.addTo(map);
  var baseLayers = { Grayscale: grayscale, Streets: streets };
  var overlays = {
    "0% - 40%": greenBins,
    "40% - 60%": yellowBins,
    "60% - 80%": orangeBins,
    "80% - 100%": redBins,
  };
  L.control.layers(baseLayers, overlays).addTo(map);
}
