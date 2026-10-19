var REFRESH_MS = 30 * 60 * 1000;
var settings = require('./settings');

function weatherMessage(payload) {
  var current = payload && payload.current;
  var daily = payload && payload.daily;
  if (!current || !daily || !Array.isArray(daily.sunset) || !daily.sunset.length ||
      !Array.isArray(daily.time) || !daily.time.length ||
      typeof current.time !== 'string' || daily.time[0] !== current.time.slice(0, 10)) return null;
  var temp = current.temperature_2m;
  var rain = current.precipitation_probability;
  var match = /T(\d\d):(\d\d)/.exec(daily.sunset[0]);
  if (typeof temp !== 'number' || !isFinite(temp) || temp < -100 || temp > 150 ||
      typeof rain !== 'number' || !isFinite(rain) || rain < 0 || rain > 100 || !match) return null;
  return {WEATHER_VALID: 1, WEATHER_TEMP: Math.round(temp),
    WEATHER_RAIN: Math.round(rain), WEATHER_SUNSET: Number(match[1]) * 60 + Number(match[2])};
}

function unavailable() { Pebble.sendAppMessage({WEATHER_VALID: 0}); }

function fetchWeather(latitude, longitude) {
  var url = 'https://api.open-meteo.com/v1/forecast?latitude=' + latitude.toFixed(4) +
    '&longitude=' + longitude.toFixed(4) +
    '&current=temperature_2m,precipitation_probability&daily=sunset' +
    '&forecast_days=1&timezone=auto&temperature_unit=fahrenheit';
  var request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.timeout = 12000;
  request.onload = function () {
    if (request.status !== 200) return unavailable();
    try {
      var message = weatherMessage(JSON.parse(request.responseText));
      if (!message) return unavailable();
      Pebble.sendAppMessage(message);
    } catch (error) { console.log('weather parse failed: ' + error); unavailable(); }
  };
  request.onerror = unavailable;
  request.ontimeout = unavailable;
  request.send();
}

function refresh() {
  if (!navigator.geolocation) return unavailable();
  navigator.geolocation.getCurrentPosition(function (position) {
    fetchWeather(position.coords.latitude, position.coords.longitude);
  }, function (error) { console.log('location failed: ' + error.message); unavailable(); },
  {timeout: 12000, maximumAge: REFRESH_MS});
}

Pebble.addEventListener('ready', function () {
  settings.initialize(function () { refresh(); setInterval(refresh, REFRESH_MS); });
});

if (typeof module !== 'undefined')
  module.exports = {weatherMessage: weatherMessage};
