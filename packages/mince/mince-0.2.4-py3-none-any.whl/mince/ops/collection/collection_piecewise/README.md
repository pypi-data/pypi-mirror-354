helper functions for use inside a `Dashboard.async_collect_data()` function

these functions will
1) collect data in time-partitioned chunks
2) store data in a time-partitioned cache

these functions use concurrency to improve performance


Tags
- each chunk receives 1 value for each tag
