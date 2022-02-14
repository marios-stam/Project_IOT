var userLong = 21.788902924716314;
var userLat = 38.288462135795776;
const start = [userLong, userLat];

mapboxgl.accessToken =
  "pk.eyJ1IjoicXdlcnRxd2VydCIsImEiOiJja3o5em84aHEwMWFuMnZwZjlyNmRjOG16In0.LQhfH1fxUa4Vds54POk2Xw";

const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/light-v10",
  center: start,
  zoom: 17,
});

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
  const arrays = await getBins();

  if (arrays[1].features.length != 0) {
    map.addSource("problems", {
      type: "geojson",
      data: arrays[1],
    });

    map.addLayer({
      id: "problems",
      type: "circle",
      source: "problems",
      paint: {
        "circle-radius": {
          stops: [
            [12, 3],
            [20, 30],
          ],
        },
        "circle-color": "#FF00FF",
      },
    });
  }

  map.addSource("bins", {
    type: "geojson",
    data: arrays[0],
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
    const arrays = await getBins(updateSource);
    map.getSource("bins").setData(arrays[0]);
    map.getSource("problems").setData(arrays[1]);
  }, 1000);

  async function getBins(updateSource) {
    try {
      r = 15;
      fetchUrl =
        "/bins_in_radius?long=" + userLong + "&lat=" + userLat + "&radius=" + r;
      const response = await fetch(fetchUrl);
      const data = await response.json();
      console.log("data:", data);
      let geojson = {
        type: "FeatureCollection",
        features: [],
      };
      let problems = {
        type: "FeatureCollection",
        features: [],
      };
      data.forEach((element) => {
        if (element.fill_level <= 0.6) {
          binColor = "green";
        } else if (element.fill_level <= 0.8) {
          binColor = "orange";
        } else {
          binColor = "red";
        }
        if (element.battery <= 0.25) {
          needCharge = true;
        } else {
          needCharge = false;
        }
        if (
          element.battery <= 0.25 ||
          element.fire_status ||
          element.fall_status
        ) {
          console.log("kek");
          problems.features.push({
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
              fall_status: element.fall_status,
              fire_status: element.fire_status,
              needCharge: needCharge,
            },
          });
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
            fall_status: element.fall_status,
            fire_status: element.fire_status,
            needCharge: needCharge,
          },
        });
      });
      return [geojson, problems];
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
  const fall_status = e.features[0].properties.fall_status;
  const fire_status = e.features[0].properties.fire_status;
  while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
    coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
  }
  let popupHTML = `<strong>Bin ID: ${sensor_id}</strong><br>Latitude: ${latitude}<br>Longitude: ${longitude}<br>Fill Level: ${fill_level.toFixed(
    1
  )}%<br>Battery: ${battery.toFixed(1)}%<br><hr>`;
  let errors = false;
  if (battery <= 25) {
    popupHTML += `🔋 This bin is low on battery! <br>`;
    errors = true;
  }
  if (fire_status) {
    popupHTML += `🔥 This bin is on fire! Call 911!<br>`;
    errors = true;
  }
  if (fall_status) {
    popupHTML += `🚯 This bin is tipped over!<br>`;
    errors = true;
  }
  if (errors) {
    popupHTML += `<hr>`;
  }
  popupHTML += `<div class="row d-flex justify-content-evenly"><a class="col-8 btn btn-danger btn-sm" href="/rpt/create/${e.features[0].properties.sensor_id}" role="button">Report Problem</a></div>`;
  new mapboxgl.Popup().setLngLat(coordinates).setHTML(popupHTML).addTo(map);
});

async function getRoute() {
  const truck_id = document.querySelector('meta[name="driver_name"]').content;
  const query2 = await fetch("/trucks/fleet_routing");
  const json2 = await query2.json();
  console.log(json2);
  let truck;
  json2.forEach((element) => {
    if (element.truck_id == truck_id) {
      truck = element;
    }
  });
  console.log(truck);
  if (truck == undefined) {
    alert("You have no routes for now");
  }
  const data2 = truck.route_coords;

  // const query2 = await fetch("/trucks/fleet_routing");
  // console.log(query2);
  // const json2 = await query2.json();
  // console.log(json2);
  // const data2 = json2[0].route_coords;
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

  const marker = new mapboxgl.Marker().setLngLat(data2[0]).addTo(map);
  map.flyTo({
    center: data2[0],
  });

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
