var userLong = 21.7351380233992;
var userLat = 38.2462665965041;
const start = [userLong, userLat];

mapboxgl.accessToken =
  "pk.eyJ1IjoicXdlcnRxd2VydCIsImEiOiJja3o5em84aHEwMWFuMnZwZjlyNmRjOG16In0.LQhfH1fxUa4Vds54POk2Xw";

const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/light-v10",
  center: start,
  zoom: 17,
});

const marker = new mapboxgl.Marker().setLngLat(start).addTo(map);

// Add custom control for bin radius to the map
class TruckFullnessControl {
  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    this._container.className = "mapboxgl-ctrl";
    this._container.innerHTML =
      '<div class="border rounded border-2 p-2 bg-gradient bg-light d-flex justify-content-center" style="border-color: #d1d1d0; width: 302px;"><label for="tfullness">Truck fullness: </label> <progress id="tfullness" value="32" max="100"> 32% </progress></div>';
    return this._container;
  }
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
map.addControl(new TruckFullnessControl(), "top-left");

class InstructionsControl {
  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    this._container.className = "mapboxgl-ctrl-directions mapboxgl-ctrl";
    this._container.innerHTML =
      '<div class="directions-control directions-control-instructions"><div class="directions-control directions-control-directions"><div class="mapbox-directions-instructions"><div id="kek" class="mapbox-directions-instructions-wrapper"></div></div></div></div>';
    return this._container;
  }
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
map.addControl(new InstructionsControl(), "top-left");

map.addControl(new mapboxgl.NavigationControl());

map.on("load", () => {
  drawBins();
  getRoute();
  checkFullness();
});



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

  const updateSource = setInterval(async () => {
    const geojson = await getBins(updateSource);
    map.getSource("bins").setData(geojson);
  }, 1000);

  async function getBins(updateSource) {
    try {
      fetchUrl = "/bins/get_all";
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
            sensor_id: element.sensor_id,
            fill_level: element.fill_level,
            battery: element.battery,
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

map.on("mouseenter", "bins", () => {
  map.getCanvas().style.cursor = "pointer";
});
map.on("mouseleave", "bins", () => {
  map.getCanvas().style.cursor = "";
});
map.on("click", "bins", (e) => {
  const coordinates = e.features[0].geometry.coordinates.slice();
  const latitude = coordinates[1].toFixed(6);
  const longitude = coordinates[0].toFixed(6);
  const sensor_id = e.features[0].properties.sensor_id;
  const fill_level = e.features[0].properties.fill_level * 100;
  const battery = e.features[0].properties.battery * 100;
  while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
    coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
  }
  const popupHTML = `<strong>Bin ID: ${sensor_id}</strong><br>Latitude: ${latitude}<br>Longitude: ${longitude}<br>Fill Level: ${fill_level.toFixed(
    1
  )}%<br>Battery: ${battery.toFixed(
    1
  )}%<br><a href="#">Report Problem</a><br><a href="/">Get Directions</a><hr><button class="btn btn-outline-success btn-sm" onclick="chargeSensor(${sensor_id})">Charge Sensor</button>`;
  new mapboxgl.Popup().setLngLat(coordinates).setHTML(popupHTML).addTo(map);
});

async function getRoute() {
  // const truck_id = document.querySelector('meta[name="driver_name"]').content;
  // const query2 = await fetch("/trucks/fleet_routing");
  // const json2 = await query2.json();
  // console.log(json2);
  // let truck;
  // json2.forEach((element) => {
  //   if (element.truck_id == truck_id) {
  //     truck = element;
  //   }
  // });

  // const data2 = truck.route_coords;
  const query2 = await fetch("/trucks/fleet_routing");
  const json2 = await query2.json();
  console.log(json2);
  const data2 = json2[0].route_coords;
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

  const end = {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        properties: {},
        geometry: {
          type: "Point",
          coordinates: data2[data2.length - 1],
        },
      },
    ],
  };
  if (map.getLayer("end")) {
    map.getSource("end").setData(end);
  } else {
    map.addLayer({
      id: "end",
      type: "circle",
      source: {
        type: "geojson",
        data: {
          type: "FeatureCollection",
          features: [
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: data2[data2.length - 1],
              },
            },
          ],
        },
      },
      paint: {
        "circle-radius": 12,
        "circle-color": "#3fb1ce",
      },
    });
  }

  const instructions = document.getElementById("kek");
  const steps = json2[0].steps;
  // const steps = truck.steps;
  let tripInstructions = "";
  steps.forEach((element) => {
    for (const step of element.steps) {
      tripInstructions += `<li class="mapbox-directions-step"><div class="mapbox-directions-step-maneuver">${step.maneuver.instruction}</div></li>`;
    }
  });
  instructions.innerHTML = `<ol class="mapbox-directions-steps">${tripInstructions}</ol>`;

  const bounds = new mapboxgl.LngLatBounds(data2[0], data2[0]);
  for (const coord of data2) {
    bounds.extend(coord);
  }
  map.fitBounds(bounds, {
    padding: 70,
  });
}

async function checkFullness() {
  const truck_id = document.querySelector('meta[name="driver_name"]').content;
  const query2 = await fetch(`/trucks/${truck_id}`);
  const json2 = await query2.json();
  document.getElementById(
    "tfullness"
  ).outerHTML = `<progress id="tfullness" value="${json2.fullness}" max="100"> ${json2.fullness}% </progress>`;
}
setInterval(checkFullness, 5000);
