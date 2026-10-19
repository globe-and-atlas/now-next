#include "schedule.h"

int nn_schedule_valid(const int starts[4]) {
  if (!starts) return 0;
  for (int i = 0; i < 4; ++i) {
    if (starts[i] < 0 || starts[i] > 23) return 0;
    if (i && starts[i] <= starts[i - 1]) return 0;
  }
  return 1;
}

int nn_period_for_hour(int hour, const int starts[4]) {
  if (hour < 0 || hour > 23 || !nn_schedule_valid(starts)) return -1;
  for (int i = 3; i >= 0; --i)
    if (hour >= starts[i]) return i;
  return 3;
}
