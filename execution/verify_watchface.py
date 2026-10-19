"""Verify Now / Next settings, schedule, weather mapping, and Emery bundle."""

import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACE = ROOT / "watchface"
TMP = ROOT / ".tmp"


def run(*args: str, cwd: Path = ROOT) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def main() -> None:
    package = json.loads((FACE / "package.json").read_text())
    assert package["pebble"]["targetPlatforms"] == ["emery"]
    assert package["pebble"]["watchapp"]["watchface"] is True
    TMP.mkdir(exist_ok=True)
    harness = TMP / "schedule_harness.c"
    harness.write_text(
        '#include <assert.h>\n#include "schedule.h"\n'
        'int main(void) { int s[4]={6,11,17,21};'
        'assert(nn_schedule_valid(s));'
        'assert(nn_period_for_hour(5,s)==3);'
        'assert(nn_period_for_hour(6,s)==0);'
        'assert(nn_period_for_hour(10,s)==0);'
        'assert(nn_period_for_hour(11,s)==1);'
        'assert(nn_period_for_hour(17,s)==2);'
        'assert(nn_period_for_hour(21,s)==3);'
        's[2]=10; assert(!nn_schedule_valid(s)); return 0; }\n'
    )
    binary = TMP / "schedule_harness"
    run("cc", "-Wall", "-Wextra", "-Werror", "-std=c99", "-I", str(FACE / "src/c"),
        str(harness), str(FACE / "src/c/schedule.c"), "-o", str(binary))
    run(str(binary))
    run("node", "-e", """
const assert = require('node:assert/strict');
global.Pebble = {addEventListener: () => {}};
const settings = require('./src/pkjs/settings');
const weather = require('./src/pkjs/index');
const values = settings.settingsMessage(JSON.stringify({SETTING_DATE:'3',
 SETTING_BG:255,SETTING_DIGITS:16777215,SETTING_ACCENT:2048,
 SETTING_START_0:'5',SETTING_START_1:'10',SETTING_START_2:'16',SETTING_START_3:'22',
 SETTING_FIELD_0:'3',SETTING_FIELD_1:'0',SETTING_FIELD_2:'1',SETTING_FIELD_3:'2'}));
assert.equal(values.SETTING_DATE,3);
assert.deepEqual([0,1,2,3].map(i=>values['SETTING_START_'+i]),[5,10,16,22]);
assert.deepEqual([0,1,2,3].map(i=>values['SETTING_FIELD_'+i]),[3,0,1,2]);
assert.equal(values.SETTING_BG,255);
assert.deepEqual([0,1,2,3].map(i=>settings.settingsMessage('{}')['SETTING_START_'+i]),[6,11,17,21]);
assert.deepEqual([0,1,2,3].map(i=>settings.settingsMessage(JSON.stringify({SETTING_START_1:22}))['SETTING_START_'+i]),[6,11,17,21]);
assert.equal(settings.config().filter(item=>item.messageKey==='SETTING_DATE')[0].options.length,4);
assert.deepEqual(weather.weatherMessage({current:{time:'2026-10-18T10:00',temperature_2m:72.4,precipitation_probability:30},daily:{time:['2026-10-18'],sunset:['2026-10-18T18:31']}}),
 {WEATHER_VALID:1,WEATHER_TEMP:72,WEATHER_RAIN:30,WEATHER_SUNSET:1111});
assert.equal(weather.weatherMessage({current:{},daily:{}}),null);
""", cwd=FACE)
    run("pebble", "build", cwd=FACE)
    bundle = FACE / "build/watchface.pbw"
    assert bundle.is_file() and bundle.stat().st_size > 0
    with zipfile.ZipFile(bundle) as archive:
        assert "appinfo.json" in archive.namelist()
    print(f"PASS {bundle}")


if __name__ == "__main__":
    main()
