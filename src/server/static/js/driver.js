var userLong = 9.997;
var userLat = 53.551;
const start = [userLong, userLat];
// var r = 1;

mapboxgl.accessToken =
  "pk.eyJ1IjoicXdlcnRxd2VydCIsImEiOiJja3o5em84aHEwMWFuMnZwZjlyNmRjOG16In0.LQhfH1fxUa4Vds54POk2Xw";

const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/light-v10",
  center: start,
  zoom: 17,
});

// var directions = new MapboxDirections({
//   accessToken: mapboxgl.accessToken,
//   interactive: false,
// });
// map.addControl(directions, "top-left");

const marker = new mapboxgl.Marker().setLngLat(start).addTo(map);

// Add zoom and rotation controls to the map
map.addControl(new mapboxgl.NavigationControl());

map.on("load", getRoute);

// Add custom control for bin radius to the map
// class BinRadiusControl {
//   onAdd(map) {
//     this._map = map;
//     this._container = document.createElement("div");
//     this._container.className = "mapboxgl-ctrl";
//     this._container.innerHTML =
//       "<div class='border rounded border-2 p-2 bg-gradient bg-light d-flex justify-content-center' style='border-color: #d1d1d0; width: 302px;'><label>Radius for bins: <select class='bin-radius' name='bin-radius'><option value='1'>1000 m</option><option value='0.5'>500 m</option><option value='0.25'>250 m</option><option value='0.125'>125 m</option></select></label></div>";
//     return this._container;
//   }
//   onRemove() {
//     this._container.parentNode.removeChild(this._container);
//     this._map = undefined;
//   }
// }
// map.addControl(new BinRadiusControl(), "top-left");

// Geolocation
// const geolocate = new mapboxgl.GeolocateControl({
//   positionOptions: {
//     enableHighAccuracy: true,
//   },
//   trackUserLocation: true,
// });
// map.addControl(geolocate);
// map.on("load", () => {
//   geolocate.trigger();
// });
// geolocate.once("geolocate", (data) => {
//   userLong = data.coords.longitude;
//   userLat = data.coords.latitude;
//   drawBins();
// });
// geolocate.on("geolocate", (data) => {
//   userLong = data.coords.longitude;
//   userLat = data.coords.latitude;
// });
// geolocate.on("error", () => {
//   console.log("An error event has occurred.");
// });
// geolocate.on("trackuserlocationstart", () => {
//   console.log("A trackuserlocationstart event has occurred.");
// });
// geolocate.on("trackuserlocationend", () => {
//   console.log("A trackuserlocationend event has occurred.");
// });

// async function drawBins() {
//   const geojson = await getBins();
//   map.addSource("bins", {
//     type: "geojson",
//     data: geojson,
//   });
//   map.addLayer({
//     id: "bins",
//     type: "circle",
//     source: "bins",
//     paint: {
//       "circle-radius": {
//         stops: [
//           [12, 2],
//           [20, 20],
//         ],
//       },
//       "circle-color": [
//         "match",
//         ["get", "color"],
//         "green",
//         "#008000",
//         "orange",
//         "#FF8000",
//         "red",
//         "#FF0000",
//         "#FF00FF",
//       ],
//     },
//   });
//   document
//     .querySelector(".bin-radius")
//     .addEventListener("change", async (event) => {
//       r = event.target.value;
//       const geojson = await getBins(updateSource);
//       map.getSource("bins").setData(geojson);
//     });
//   const updateSource = setInterval(async () => {
//     const geojson = await getBins(updateSource);
//     map.getSource("bins").setData(geojson);
//   }, 10000);
//   async function getBins(updateSource) {
//     try {
//       fetchUrl =
//         "/bins_in_radius?long=" + userLong + "&lat=" + userLat + "&radius=" + r;
//       const response = await fetch(fetchUrl);
//       const data = await response.json();
//       let geojson = {
//         type: "FeatureCollection",
//         features: [],
//       };
//       data.forEach((element) => {
//         if (element.fill_level <= 60) {
//           binColor = "green";
//         } else if (element.fill_level <= 80) {
//           binColor = "orange";
//         } else {
//           binColor = "red";
//         }
//         geojson.features.push({
//           type: "Feature",
//           geometry: {
//             type: "Point",
//             coordinates: [element.long, element.lat],
//           },
//           properties: {
//             color: binColor,
//             entry_id: element.entry_id,
//             fill_level: element.fill_level,
//             battery: element.battery,
//           },
//         });
//       });
//       return geojson;
//     } catch (err) {
//       if (updateSource) clearInterval(updateSource);
//       throw new Error(err);
//     }
//   }
// }

// map.on("mouseenter", "bins", () => {
//   map.getCanvas().style.cursor = "pointer";
// });
// map.on("mouseleave", "bins", () => {
//   map.getCanvas().style.cursor = "";
// });
// map.on("click", "bins", (e) => {
//   const coordinates = e.features[0].geometry.coordinates.slice();
//   const latitude = coordinates[1].toFixed(6);
//   const longitude = coordinates[0].toFixed(6);
//   const entry_id = e.features[0].properties.entry_id;
//   const fill_level = e.features[0].properties.fill_level;
//   const battery = e.features[0].properties.battery;
//   while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
//     coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
//   }
//   const popupHTML = `<strong>Bin ID: ${entry_id}</strong><br>Latitude: ${latitude}<br>Longitude: ${longitude}<br>Fill Level: ${fill_level}%<br>Battery: ${battery}%<br><a href="#">Report Problem</a><br><a href="#">Get Directions</a><hr><a href="#">Throw Garbage</a><br><a href="#">Charge Sensor</a>`;
//   new mapboxgl.Popup().setLngLat(coordinates).setHTML(popupHTML).addTo(map);
// });

async function getRoute() {
  const query2 = await fetch("/client/driver/routing?truck_id=1");
  const json2 = await query2.json();
  const data2 = json2.route_coords;
  console.log(data2);
  const geojson = {
    type: "Feature",
    properties: {},
    geometry: {
      type: "LineString",
      coordinates: data2,
    },
  };
  if (map.getSource("route")) {
    map.getSource("route").setData(geojson);
  } else {
    map.addLayer({
      id: "route",
      type: "line",
      source: {
        type: "geojson",
        data: geojson,
      },
      layout: {
        "line-join": "round",
        "line-cap": "round",
      },
      paint: {
        "line-color": "#3887be",
        "line-width": 5,
        "line-opacity": 0.75,
      },
    });
  }
  // const instructions = document.getElementById("instructions");
  // const steps = data.legs[0].steps;
  // let tripInstructions = "";
  // for (const step of steps) {
  //   tripInstructions += `<li>${step.maneuver.instruction}</li>`;
  // }
  // instructions.innerHTML = `<p><strong>Trip duration: ${Math.floor(
  //   data.duration / 60
  // )} min </strong></p><ol>${tripInstructions}</ol>`;
}
