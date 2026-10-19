#ifndef NOW_NEXT_SCHEDULE_H
#define NOW_NEXT_SCHEDULE_H

/* Starts are ascending in local wall-clock hours; the last period wraps midnight. */
int nn_schedule_valid(const int starts[4]);
int nn_period_for_hour(int hour, const int starts[4]);

#endif
