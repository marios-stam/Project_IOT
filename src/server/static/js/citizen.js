var userLong, userLat, start;
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

var directions = new MapboxDirections({
  accessToken: mapboxgl.accessToken,
  unit: "metric",
  profile: "mapbox/walking",
  interactive: false,
});
map.addControl(directions);

// Add zoom and rotation controls to the map
map.addControl(new mapboxgl.NavigationControl());

// Add custom control for bin radius to the map
class BinRadiusControl {
  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    this._container.className = "mapboxgl-ctrl";
    this._container.innerHTML =
      "<div class='border rounded border-2 p-2 bg-gradient bg-light d-flex justify-content-center' style='border-color: #d1d1d0; width: 302px;'><label>Radius for bins: <select class='bin-radius' name='bin-radius'><option value='5'>5,000 m</option><option value='2.5'>2,500 m</option><option value='1' selected>1,000 m</option><option value='0.5'>500 m</option><option value='0.25'>250 m</option>";
    return this._container;
  }
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
map.addControl(new BinRadiusControl(), "top-left");

class BountiesControl {
  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    this._container.className = "mapboxgl-ctrl";
    this._container.innerHTML =
      '<div class="border rounded border-2 p-2 bg-gradient bg-light d-flex justify-content-center" style="border-color: #d1d1d0; width: 302px;"><button type="button" class="border border-secondary rounded" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Check for bounties near you</button></div>';
    return this._container;
  }
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
map.addControl(new BountiesControl(), "top-left");

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
  start = [userLong, userLat];
  drawBins();
  getBounties();
});
geolocate.on("geolocate", (data) => {
  userLong = data.coords.longitude;
  userLat = data.coords.latitude;
  start = [userLong, userLat];
});
geolocate.on("error", () => {
  console.log("An error event has occurred.");
  userLong = 21.73513802339923;
  userLat = 38.24626659650408;
  start = [userLong, userLat];
  new mapboxgl.Marker().setLngLat([userLong, userLat]).addTo(map);
  drawBins();
  getBounties();
});
// geolocate.on("trackuserlocationstart", () => {
//   console.log("A trackuserlocationstart event has occurred.");
// });
// geolocate.on("trackuserlocationend", () => {
//   console.log("A trackuserlocationend event has occurred.");
// });

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

  document
    .querySelector(".bin-radius")
    .addEventListener("change", async (event) => {
      r = event.target.value;
      const arrays = await getBins(updateSource);
      map.getSource("bins").setData(arrays[0]);
      map.getSource("problems").setData(arrays[1]);
    });

  const updateSource = setInterval(async () => {
    const arrays = await getBins(updateSource);
    map.getSource("bins").setData(arrays[0]);
    map.getSource("problems").setData(arrays[1]);
  }, 1000000);

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
      let problems = {
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
        needCharge = false;
        if (
          element.battery <= 0.25 ||
          element.fire_status ||
          element.fall_status
        ) {
          needCharge = true;
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
  popupHTML += `<div class="row d-flex justify-content-evenly"><button class="col-5 btn btn-primary btn-sm" onclick="getDirections('${e.features[0].properties.sensor_id}')">Get Directions</button><a class="col-5 btn btn-danger btn-sm" href="/rpt/create/${e.features[0].properties.sensor_id}" role="button">Report Problem</a></div>`;
  new mapboxgl.Popup().setLngLat(coordinates).setHTML(popupHTML).addTo(map);
});

async function getBounties() {
  try {
    // const sdata = { long: userLong, lat: userLat, radius: r };
    // const response = await fetch("/bounties/in_radius", {
    let sdata = { long: userLong, lat: userLat, radius: r };
    console.log(sdata);
    let response = await fetch("/bounties/in_radius", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sdata),
    });
    // const rdata = await response.json();
    let rdata = await response.json();
    offcanvasBody = document.querySelector(".offcanvas-body");
    offcanvasBody.innerHTML = "";
    let mybounties = "";
    let otherbounties = "";
    rdata.forEach((element, index, array) => {
      if (
        element.assigned_usr_id ==
        document.querySelector('meta[name="user_id"]').content
      ) {
        let now = Date.now();
        let ass = Date.parse(element.time_assigned + " GMT+2");
        let left = new Date(ass + 3600000 - now);
        let timeLeft =
          ("0" + left.getUTCHours()).slice(-2) +
          ":" +
          ("0" + left.getUTCMinutes()).slice(-2) +
          ":" +
          ("0" + left.getUTCSeconds()).slice(-2);
        mybounties += `<p class="bg-success"><strong>${element.message}</strong><br>Bin ID: ${element.bin_id}<br>Added At: ${element.timestamp}<br></p><p><button onclick="getDirections('${element.bin_id}')">Get Directions</button> <em>Reward: ${element.points} pts</em></p><p>Time left: ${timeLeft}</p><hr>`;
      }
      if (element.assigned_usr_id == null) {
        otherbounties += `<p><strong>${element.message}</strong><br>Bin ID: ${element.bin_id}<br>Added At: ${element.timestamp}<br></p><p><button onclick=assumeBounty(${element.id})>Take over the handling</button> <em>Reward: ${element.points} pts</em></p><hr>`;
      }
    });
    offcanvasBody.innerHTML = mybounties + otherbounties;
  } catch (error) {
    console.log("Error: ", error);
  }
}
setInterval(getBounties, 2000);

async function getDirections(binId) {
  directions.removeRoutes();
  const response = await fetch(fetchUrl);
  const data = await response.json();
  let binLong, binLat;
  data.forEach((element) => {
    if (element.sensor_id == binId) {
      binLong = element.long;
      binLat = element.lat;
    }
  });
  directions.setOrigin(start);
  directions.setDestination([binLong, binLat]);
}

async function assumeBounty(bountyId) {
  try {
    const sdata = {
      id: bountyId,
      assigned_usr_id: document.querySelector('meta[name="user_id"]').content,
    };
    const response = await fetch("/bounties/assign_bounty", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sdata),
    });
    // console.log(response)
    // offcanvasBody = document.querySelector(".offcanvas-body");
    // offcanvasBody.innerHTML = "";
    // rdata.forEach((element) => {
    //   offcanvasBody.innerHTML += `<p><strong>${element.message}</strong><br>Bin ID: ${element.bin_id}<br>Added At: ${element.timestamp}<br></p><p><button>Take over the handling</button> <em>Reward: ${element.points} pts</em></p><hr>`;
    // });
    // console.log(rdata);
  } catch (error) {
    console.log("Error: ", error);
  }
}
