## cdf 

### Fixed

- When running `cdf deploy`, Toolkit no longer overwrites nodes that are
existing. Instead they are updated. This means if there is a property
that is not in the local configuration but is set in CDF, Toolkit will
not overwrite.

## templates

No changes.