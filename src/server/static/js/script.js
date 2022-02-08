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

var map, grayscale, streets;
initializeMap().then(findLocation);

async function initializeMap() {
  map = L.map("map");
  var mbAttr =
    '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>';
  var mbUrl =
    "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}";
  grayscale = L.tileLayer(mbUrl, {
    id: "mapbox/light-v10",
    tileSize: 512,
    zoomOffset: -1,
    attribution: mbAttr,
    accessToken:
      "pk.eyJ1IjoicXdlcnRxd2VydCIsImEiOiJja3o5em84aHEwMWFuMnZwZjlyNmRjOG16In0.LQhfH1fxUa4Vds54POk2Xw",
  });
  streets = L.tileLayer(mbUrl, {
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    attribution: mbAttr,
    accessToken:
      "pk.eyJ1IjoicXdlcnRxd2VydCIsImEiOiJja3o5em84aHEwMWFuMnZwZjlyNmRjOG16In0.LQhfH1fxUa4Vds54POk2Xw",
  });
  grayscale.addTo(map);
}

// Geolocation
async function findLocation() {
  map.locate({ setView: true, maxZoom: 16 });
  map.on("locationfound", onLocationFound);
  map.on("locationerror", onLocationError);
}
function onLocationFound(e) {
  var radius = e.accuracy;
  L.marker(e.latlng).addTo(map).bindPopup("You are here").openPopup();
  L.circle(e.latlng, radius).addTo(map);
  getBins(e.latlng)
    .then(setInterval(updateBins, 10000))
    .catch((error) => {
      alert(
        "Oops! Error while retrieving bins information. Please try again later."
      );
      console.log(error);
    });
}
function onLocationError(e) {
  alert(e.message);
  map.setView([51.505, -0.09], 13);
  L.marker([51.5, -0.09]).addTo(map);
  getBins({ lng: -0.09, lat: 51.505 })
    .then(setInterval(updateBins, 10000))
    .catch((error) => {
      alert(
        "Oops! Error while retrieving bins information. Please try again later."
      );
      console.log(error);
    });
}
//*/ map.setView(loc, 18);

// Create bin layer groups
var greenLayerGroup = L.layerGroup();
var yellowLayerGroup = L.layerGroup();
var orangeLayerGroup = L.layerGroup();
var redLayerGroup = L.layerGroup();

// Create GeoJSON layers
var greenGeoJSONLayer, yellowGeoJSONLayer, orangeGeoJSONLayer, redGeoJSONLayer;

// Fetch bins list, then create corresponding markers, then create the layers controls
var r = 1;
var latlong;
async function getBins(loc) {
  latlong = loc;
  fetch("/bins_in_radius?long=" + loc.lng + "&lat=" + loc.lat + "&radius=" + r)
    .then((response) => response.json())
    .then((data) => {
      data.forEach(this.createBinMarkers);
    })
    .then(() => {
      this.createLayersControl();
    });
}
function createBinMarkers(obj, index, array) {
  var geoJSON = {
    type: "Feature",
    properties: {
      fullness: obj.fullness,
      id: obj.id,
      record_id: obj.record_id,
      status: obj.status,
      updated: obj.updated,
    },
    geometry: { type: "Point", coordinates: [obj.longtitude, obj.latitude] },
  };
  var fullness = obj.fullness;
  if (fullness <= 40) {
    greenGeoJSONLayer = L.geoJSON(geoJSON, {
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
      .addTo(greenLayerGroup);
  } else if (fullness <= 60) {
    yellowGeoJSONLayer = L.geoJSON(geoJSON, {
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
      .addTo(yellowLayerGroup);
  } else if (fullness <= 80) {
    orangeGeoJSONLayer = L.geoJSON(geoJSON, {
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
      .addTo(orangeLayerGroup);
  } else {
    redGeoJSONLayer = L.geoJSON(geoJSON, {
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
      .addTo(redLayerGroup);
  }
}
function createLayersControl() {
  greenLayerGroup.addTo(map);
  yellowLayerGroup.addTo(map);
  orangeLayerGroup.addTo(map);
  redLayerGroup.addTo(map);
  var baseLayers = { Grayscale: grayscale, Streets: streets };
  var overlays = {
    "0% - 40%": greenLayerGroup,
    "40% - 60%": yellowLayerGroup,
    "60% - 80%": orangeLayerGroup,
    "80% - 100%": redLayerGroup,
  };
  L.control.layers(baseLayers, overlays).addTo(map);
}

// Update bins information repeatedly, with a 10 seconds delay between.
async function updateBins() {
  const response = await fetch(
    "/bins_in_radius?long=" +
      latlong.lng +
      "&lat=" +
      latlong.lat +
      "&radius=" +
      r
  );
  const data = await response.json();
  greenGeoJSONLayer.clearLayers();
  greenLayerGroup.clearLayers();
  yellowGeoJSONLayer.clearLayers();
  yellowLayerGroup.clearLayers();
  orangeGeoJSONLayer.clearLayers();
  orangeLayerGroup.clearLayers();
  redGeoJSONLayer.clearLayers();
  redLayerGroup.clearLayers();
  data.forEach(this.createBinMarkers);
}

// Clicking on map and see coordinates
function onMapClick(e) {
  L.popup()
    .setLatLng(e.latlng)
    .setContent("You clicked the map at " + e.latlng.toString())
    .openOn(map);
}
map.on("click", onMapClick);
//*/

// Change radius of search
document.querySelector(".bin-radius").addEventListener("change", (event) => {
  r = event.target.value;
  updateBins();
});
