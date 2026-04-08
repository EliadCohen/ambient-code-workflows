# /stop-monitor - Stop Monitoring

## Purpose

Stop the active monitoring loop.

## Prerequisites

- Monitoring is currently active

## Process

1. Cancel the recurring cron job
2. Confirm monitoring has stopped
3. Show final statistics (total ideas tracked)

## Output

- Confirmation message
- Summary of ideas collected

## Example

```
/stop-monitor
```
