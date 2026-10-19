var FIELD_NAMES = ['Rain chance', 'Temperature', 'Sunset', 'Watch battery'];
var PERIOD_NAMES = ['Morning', 'Daytime', 'Evening', 'Night'];
var START_DEFAULTS = [6, 11, 17, 21];
var FIELD_DEFAULTS = [0, 1, 2, 3];
var COLORS = { SETTING_BG: 0x102834, SETTING_DIGITS: 0xF6F1DE, SETTING_ACCENT: 0x6FD6C0 };

function integer(value, min, max, fallback) {
  var n = Number(value);
  return isFinite(n) && Math.floor(n) === n && n >= min && n <= max ? n : fallback;
}

function settingsMessage(raw) {
  var saved;
  try { saved = JSON.parse(raw) || {}; } catch (error) { saved = {}; }
  var result = { SETTING_DATE: integer(saved.SETTING_DATE, 0, 3, 1) };
  Object.keys(COLORS).forEach(function (key) {
    result[key] = integer(saved[key], 0, 0xFFFFFF, COLORS[key]);
  });
  var starts = START_DEFAULTS.map(function (value, i) {
    return integer(saved['SETTING_START_' + i], 0, 23, value);
  });
  if (!(starts[0] < starts[1] && starts[1] < starts[2] && starts[2] < starts[3]))
    starts = START_DEFAULTS.slice();
  starts.forEach(function (value, i) {
    result['SETTING_START_' + i] = value;
    result['SETTING_FIELD_' + i] = integer(saved['SETTING_FIELD_' + i], 0, 3, FIELD_DEFAULTS[i]);
  });
  return result;
}

function config() {
  var items = [
    {type: 'heading', defaultValue: 'Now / Next'},
    {type: 'text', defaultValue: 'One useful detail at a time. Choose when each period begins.'},
    {type: 'heading', defaultValue: 'Appearance'},
    {type: 'color', messageKey: 'SETTING_BG', label: 'Background', defaultValue: '102834', sunlight: false, allowGray: true},
    {type: 'color', messageKey: 'SETTING_DIGITS', label: 'Clock digits', defaultValue: 'F6F1DE', sunlight: false, allowGray: true},
    {type: 'color', messageKey: 'SETTING_ACCENT', label: 'Accent', defaultValue: '6FD6C0', sunlight: false, allowGray: true},
    {type: 'select', messageKey: 'SETTING_DATE', label: 'Date', defaultValue: '1', options: [
      {label: 'Off', value: '0'}, {label: 'YYYY-MM-DD', value: '1'},
      {label: 'MM/DD/YYYY', value: '2'}, {label: 'DD/MM/YYYY', value: '3'}
    ]}
  ];
  PERIOD_NAMES.forEach(function (name, i) {
    var hours = [];
    for (var hour = 0; hour < 24; ++hour)
      hours.push({label: (hour < 10 ? '0' : '') + hour + ':00', value: String(hour)});
    items.push({type: 'heading', defaultValue: name});
    items.push({type: 'select', messageKey: 'SETTING_START_' + i,
      label: 'Starts at', defaultValue: String(START_DEFAULTS[i]), options: hours});
    items.push({type: 'select', messageKey: 'SETTING_FIELD_' + i,
      label: 'Show', defaultValue: String(FIELD_DEFAULTS[i]),
      options: FIELD_NAMES.map(function (field, index) { return {label: field, value: String(index)}; })});
  });
  items.push({type: 'text', defaultValue: 'Start times must increase from morning to night. Invalid schedules reset to 06:00, 11:00, 17:00, 21:00.'});
  items.push({type: 'submit', defaultValue: 'Save to watch'});
  return items;
}

function initialize(onReady) {
  var Clay = require('@rebble/clay');
  var clay = new Clay(config(), null, {autoHandleEvents: false});
  function send(raw) {
    Pebble.sendAppMessage(settingsMessage(raw), null, function (error) {
      console.log('settings send failed: ' + JSON.stringify(error));
    });
  }
  Pebble.addEventListener('showConfiguration', function () { Pebble.openURL(clay.generateUrl()); });
  Pebble.addEventListener('webviewclosed', function (event) {
    if (!event || !event.response || event.response === 'CANCELLED') return;
    try { clay.getSettings(event.response); }
    catch (error) { console.log('settings rejected: ' + error); return; }
    send(localStorage.getItem('clay-settings'));
  });
  var saved = localStorage.getItem('clay-settings');
  if (saved) send(saved);
  if (onReady) onReady();
}

module.exports = { initialize: initialize, settingsMessage: settingsMessage, config: config };
