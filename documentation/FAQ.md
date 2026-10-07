# Frequently Asked Questions

## Why is the first CPU reading low?

psutil initializes its non-blocking CPU counter on first use. Subsequent samples reflect the configured interval.

## Does the app close processes?

No. It only reports local resource information.
