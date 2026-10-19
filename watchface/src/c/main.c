#include <pebble.h>
#include "schedule.h"

#define FACE_W 200
#define FACE_H 228
#define WEATHER_STALE_SECONDS 3600
#define PERSIST_BG 1
#define PERSIST_DIGITS 2
#define PERSIST_ACCENT 3
#define PERSIST_DATE 4
#define PERSIST_START_BASE 10
#define PERSIST_FIELD_BASE 20

static Window *s_window;
static Layer *s_layer;
static int s_bg = 0x102834;
static int s_digits = 0xF6F1DE;
static int s_accent = 0x6FD6C0;
static int s_date = 1;
static int s_starts[4] = {6, 11, 17, 21};
static int s_fields[4] = {0, 1, 2, 3};
static int s_temperature;
static int s_rain;
static int s_sunset;
static time_t s_weather_at;
static const char *s_periods[4] = {"MORNING", "DAYTIME", "EVENING", "NIGHT"};
static uint32_t start_key(int index) {
  if (index == 0) return MESSAGE_KEY_SETTING_START_0;
  if (index == 1) return MESSAGE_KEY_SETTING_START_1;
  if (index == 2) return MESSAGE_KEY_SETTING_START_2;
  return MESSAGE_KEY_SETTING_START_3;
}

static uint32_t field_key(int index) {
  if (index == 0) return MESSAGE_KEY_SETTING_FIELD_0;
  if (index == 1) return MESSAGE_KEY_SETTING_FIELD_1;
  if (index == 2) return MESSAGE_KEY_SETTING_FIELD_2;
  return MESSAGE_KEY_SETTING_FIELD_3;
}

static void fill(GContext *ctx, int x, int y, int w, int h, GColor color) {
  graphics_context_set_fill_color(ctx, color);
  graphics_fill_rect(ctx, GRect(x, y, w, h), 0, GCornerNone);
}

static void label(GContext *ctx, const char *value, const char *font,
                  GRect rect, GColor color, GTextAlignment alignment) {
  graphics_context_set_text_color(ctx, color);
  graphics_draw_text(ctx, value, fonts_get_system_font(font), rect,
                     GTextOverflowModeTrailingEllipsis, alignment, NULL);
}

static bool weather_fresh(time_t now) {
  return s_weather_at && now >= s_weather_at &&
         now - s_weather_at <= WEATHER_STALE_SECONDS;
}

static void context_text(int field, time_t now, char *value, size_t size) {
  if (field == 3) {
    snprintf(value, size, "%d%%", battery_state_service_peek().charge_percent);
  } else if (!weather_fresh(now)) {
    snprintf(value, size, "UNAVAILABLE");
  } else if (field == 0) {
    snprintf(value, size, "%d%%", s_rain);
  } else if (field == 1) {
    snprintf(value, size, "%dF", s_temperature);
  } else {
    int hour = s_sunset / 60;
    if (clock_is_24h_style())
      snprintf(value, size, "%02d:%02d", hour, s_sunset % 60);
    else
      snprintf(value, size, "%d:%02d%s", (hour % 12) ? hour % 12 : 12,
               s_sunset % 60, hour < 12 ? "A" : "P");
  }
}

static const char *field_name(int field) {
  static const char *names[4] = {"RAIN CHANCE", "TEMPERATURE", "SUNSET", "BATTERY"};
  return names[field >= 0 && field <= 3 ? field : 3];
}

static const char *field_short_name(int field) {
  static const char *names[4] = {"RAIN", "TEMP", "SUNSET", "BATTERY"};
  return names[field >= 0 && field <= 3 ? field : 3];
}

static void draw(Layer *layer, GContext *ctx) {
  (void)layer;
  GColor bg = GColorFromHEX(s_bg);
  GColor digits = GColorFromHEX(s_digits);
  GColor accent = GColorFromHEX(s_accent);
  fill(ctx, 0, 0, FACE_W, FACE_H, bg);
  fill(ctx, 15, 14, 22, 4, accent);
  label(ctx, "NOW / NEXT", FONT_KEY_GOTHIC_18_BOLD, GRect(43, 6, 143, 26),
        accent, GTextAlignmentRight);

  time_t now = time(NULL);
  struct tm *local = localtime(&now);
  char clock_text[12];
  strftime(clock_text, sizeof(clock_text), clock_is_24h_style() ? "%H:%M" : "%I:%M", local);
  if (!clock_is_24h_style() && clock_text[0] == '0')
    memmove(clock_text, clock_text + 1, strlen(clock_text));
  label(ctx, clock_text, FONT_KEY_LECO_60_BOLD_NUMBERS_AM_PM,
        GRect(4, 35, 192, 79), digits, GTextAlignmentCenter);

  if (s_date) {
    char date[16];
    const char *format = s_date == 1 ? "%Y-%m-%d" :
                         s_date == 2 ? "%m/%d/%Y" : "%d/%m/%Y";
    strftime(date, sizeof(date), format, local);
    label(ctx, date, FONT_KEY_GOTHIC_18_BOLD, GRect(12, 109, 176, 27),
          digits, GTextAlignmentCenter);
  }

  fill(ctx, 16, 137, 168, 2, accent);
  int period = nn_period_for_hour(local->tm_hour, s_starts);
  if (period < 0) period = 3;
  char heading[40];
  if (s_fields[period] == 3)
    snprintf(heading, sizeof(heading), "%s", s_periods[period]);
  else
    snprintf(heading, sizeof(heading), "%s  /  %s", s_periods[period], field_name(s_fields[period]));
  label(ctx, heading, FONT_KEY_GOTHIC_14_BOLD, GRect(12, 144, 176, 23),
        accent, GTextAlignmentCenter);
  char value[32];
  context_text(s_fields[period], now, value, sizeof(value));
  label(ctx, value, FONT_KEY_GOTHIC_28_BOLD, GRect(8, 165, 184, 40),
        digits, GTextAlignmentCenter);

  int next = (period + 1) % 4;
  char footer[40];
  int start = s_starts[next];
  if (clock_is_24h_style())
    snprintf(footer, sizeof(footer), "NEXT %s %02d:00", field_short_name(s_fields[next]), start);
  else
    snprintf(footer, sizeof(footer), "NEXT %s %d%s", field_short_name(s_fields[next]),
             (start % 12) ? start % 12 : 12, start < 12 ? "AM" : "PM");
  label(ctx, footer, FONT_KEY_GOTHIC_14_BOLD, GRect(8, 205, 184, 21),
        accent, GTextAlignmentCenter);
}

static void tick(struct tm *time_now, TimeUnits units) {
  (void)time_now; (void)units;
  layer_mark_dirty(s_layer);
}

static void battery(BatteryChargeState state) {
  (void)state;
  layer_mark_dirty(s_layer);
}

static void read_color(DictionaryIterator *iter, uint32_t key, int *target, int persist_key) {
  Tuple *tuple = dict_find(iter, key);
  if (tuple && tuple->value->int32 >= 0 && tuple->value->int32 <= 0xFFFFFF) {
    *target = tuple->value->int32;
    persist_write_int(persist_key, *target);
  }
}

static void inbox(DictionaryIterator *iter, void *context) {
  (void)context;
  read_color(iter, MESSAGE_KEY_SETTING_BG, &s_bg, PERSIST_BG);
  read_color(iter, MESSAGE_KEY_SETTING_DIGITS, &s_digits, PERSIST_DIGITS);
  read_color(iter, MESSAGE_KEY_SETTING_ACCENT, &s_accent, PERSIST_ACCENT);
  Tuple *date = dict_find(iter, MESSAGE_KEY_SETTING_DATE);
  if (date && date->value->int32 >= 0 && date->value->int32 <= 3) {
    s_date = date->value->int32;
    persist_write_int(PERSIST_DATE, s_date);
  }
  int starts[4];
  for (int i = 0; i < 4; ++i) {
    starts[i] = s_starts[i];
    Tuple *tuple = dict_find(iter, start_key(i));
    if (tuple) starts[i] = tuple->value->int32;
  }
  if (nn_schedule_valid(starts)) {
    for (int i = 0; i < 4; ++i) {
      s_starts[i] = starts[i];
      persist_write_int(PERSIST_START_BASE + i, s_starts[i]);
    }
  }
  for (int i = 0; i < 4; ++i) {
    Tuple *tuple = dict_find(iter, field_key(i));
    if (tuple && tuple->value->int32 >= 0 && tuple->value->int32 <= 3) {
      s_fields[i] = tuple->value->int32;
      persist_write_int(PERSIST_FIELD_BASE + i, s_fields[i]);
    }
  }
  Tuple *valid = dict_find(iter, MESSAGE_KEY_WEATHER_VALID);
  if (valid) {
    if (!valid->value->int32) s_weather_at = 0;
    else {
      Tuple *temperature = dict_find(iter, MESSAGE_KEY_WEATHER_TEMP);
      Tuple *rain = dict_find(iter, MESSAGE_KEY_WEATHER_RAIN);
      Tuple *sunset = dict_find(iter, MESSAGE_KEY_WEATHER_SUNSET);
      if (temperature && rain && sunset &&
          temperature->value->int32 >= -100 && temperature->value->int32 <= 150 &&
          rain->value->int32 >= 0 && rain->value->int32 <= 100 &&
          sunset->value->int32 >= 0 && sunset->value->int32 < 1440) {
        s_temperature = temperature->value->int32;
        s_rain = rain->value->int32;
        s_sunset = sunset->value->int32;
        s_weather_at = time(NULL);
      }
    }
  }
  layer_mark_dirty(s_layer);
}

static void load(Window *window) {
  s_layer = layer_create(GRect(0, 0, FACE_W, FACE_H));
  layer_set_update_proc(s_layer, draw);
  layer_add_child(window_get_root_layer(window), s_layer);
}

static void unload(Window *window) {
  (void)window;
  layer_destroy(s_layer);
}

int main(void) {
  if (persist_exists(PERSIST_BG)) s_bg = persist_read_int(PERSIST_BG);
  if (persist_exists(PERSIST_DIGITS)) s_digits = persist_read_int(PERSIST_DIGITS);
  if (persist_exists(PERSIST_ACCENT)) s_accent = persist_read_int(PERSIST_ACCENT);
  if (persist_exists(PERSIST_DATE)) s_date = persist_read_int(PERSIST_DATE);
  if (s_bg < 0 || s_bg > 0xFFFFFF) s_bg = 0x102834;
  if (s_digits < 0 || s_digits > 0xFFFFFF) s_digits = 0xF6F1DE;
  if (s_accent < 0 || s_accent > 0xFFFFFF) s_accent = 0x6FD6C0;
  if (s_date < 0 || s_date > 3) s_date = 1;
  for (int i = 0; i < 4; ++i) {
    if (persist_exists(PERSIST_START_BASE + i)) s_starts[i] = persist_read_int(PERSIST_START_BASE + i);
    if (persist_exists(PERSIST_FIELD_BASE + i)) s_fields[i] = persist_read_int(PERSIST_FIELD_BASE + i);
    if (s_fields[i] < 0 || s_fields[i] > 3) s_fields[i] = i;
  }
  if (!nn_schedule_valid(s_starts)) {
    const int defaults[4] = {6, 11, 17, 21};
    memcpy(s_starts, defaults, sizeof(defaults));
  }
  s_window = window_create();
  window_set_window_handlers(s_window, (WindowHandlers){.load = load, .unload = unload});
  window_stack_push(s_window, true);
  tick_timer_service_subscribe(MINUTE_UNIT, tick);
  battery_state_service_subscribe(battery);
  app_message_register_inbox_received(inbox);
  app_message_open(256, 64);
  app_event_loop();
  app_message_deregister_callbacks();
  battery_state_service_unsubscribe();
  tick_timer_service_unsubscribe();
  window_destroy(s_window);
}
