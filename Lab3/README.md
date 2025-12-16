// Name: Hazal Guc
// StudentID: 231ADB264
// Lab: Programming Languages - Lab 3
# gosort – Concurrent Chunk Sorting (Lab 3)

This program sorts integers concurrently using Go routines.
The input is split into chunks, each chunk is sorted in its own goroutine,
and the sorted chunks are merged into one globally sorted result.

## How to run

Run all commands from the `Lab3` directory.

### Mode 1: Random numbers
```bash
go run . -r N
