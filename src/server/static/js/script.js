var userLong, userLat;
var r = 1;

// Get and set the map's access token
mapboxgl.accessToken =
  "pk.eyJ1IjoicXdlcnRxd2VydCIsImEiOiJja3o5em84aHEwMWFuMnZwZjlyNmRjOG16In0.LQhfH1fxUa4Vds54POk2Xw";

// Initialize the map
const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/light-v10",
  center: [21.735, 38.246],
  zoom: 17,
});

// Add zoom and rotation controls to the map
map.addControl(new mapboxgl.NavigationControl());

// Add custom control for bin radius to the map
class BinRadiusControl {
  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    this._container.className = "mapboxgl-ctrl";
    this._container.innerHTML =
      "<div class='border rounded border-2 p-2 bg-gradient bg-light' style='border-color: #d1d1d0;'><label>Radius for bins: <select class='bin-radius' name='bin-radius'><option value='1'>1000 m</option><option value='0.5'>500 m</option><option value='0.25'>250 m</option><option value='0.125'>125 m</option></select></label></div>";
    return this._container;
  }
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
map.addControl(new BinRadiusControl(), "top-left");

// Geolocation
const geolocate = new mapboxgl.GeolocateControl({
  positionOptions: {
    enableHighAccuracy: true,
  },
  trackUserLocation: true,
});
map.addControl(geolocate);
map.on("load", () => {
  geolocate.trigger();
});
geolocate.once("geolocate", (data) => {
  userLong = data.coords.longitude;
  userLat = data.coords.latitude;
  console.log(userLong, userLat);
  console.log("A geolocate event has occurred.");
  drawBins();
});
geolocate.on("geolocate", (data) => {
  userLong = data.coords.longitude;
  userLat = data.coords.latitude;
});
// geolocate.on("error", () => {
//   console.log("An error event has occurred.");
// });
// geolocate.on("trackuserlocationstart", () => {
//   console.log("A trackuserlocationstart event has occurred.");
// });
// geolocate.on("trackuserlocationend", () => {
//   console.log("A trackuserlocationend event has occurred.");
// });

async function drawBins() {
  const geojson = await getBins();

  map.addSource("bins", {
    type: "geojson",
    data: geojson,
  });

  map.addLayer({
    id: "bins",
    type: "circle",
    source: "bins",
    paint: {
      "circle-radius": {
        stops: [
          [12, 2],
          [20, 20],
        ],
      },
      "circle-color": [
        "match",
        ["get", "color"],
        "green",
        "#008000",
        "orange",
        "#FF8000",
        "red",
        "#FF0000",
        "#FF00FF",
      ],
    },
  });

  document
    .querySelector(".bin-radius")
    .addEventListener("change", async (event) => {
      r = event.target.value;
      const geojson = await getBins(updateSource);
      map.getSource("bins").setData(geojson);
    });

  const updateSource = setInterval(async () => {
    const geojson = await getBins(updateSource);
    map.getSource("bins").setData(geojson);
  }, 10000);

  async function getBins(updateSource) {
    try {
      fetchUrl =
        "/bins_in_radius?long=" + userLong + "&lat=" + userLat + "&radius=" + r;
      const response = await fetch(fetchUrl);
      const data = await response.json();
      let geojson = {
        type: "FeatureCollection",
        features: [],
      };
      data.forEach((element) => {
        if (element.fill_level <= 60) {
          binColor = "green";
        } else if (element.fill_level <= 80) {
          binColor = "orange";
        } else {
          binColor = "red";
        }
        geojson.features.push({
          type: "Feature",
          geometry: {
            type: "Point",
            coordinates: [element.long, element.lat],
          },
          properties: {
            color: binColor,
          },
        });
      });
      return geojson;
    } catch (err) {
      if (updateSource) clearInterval(updateSource);
      throw new Error(err);
    }
  }
}
