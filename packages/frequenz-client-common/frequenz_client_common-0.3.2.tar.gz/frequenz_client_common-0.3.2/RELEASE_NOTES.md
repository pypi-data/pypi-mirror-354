# Frequenz Client Common Library Release Notes

## Summary

This release replaces the failed v0.3.1 release.

## Upgrading

- The `typing-extensions` dependency minimum version was bumped to 4.13 to support Python 3.12.

## New Features

- New `BaseId` class to create unique IDs for entities in the system.
- New ID classes for microgrid-related entities:

   * `EnterpriseId`
   * `MicrogridId`
   * `ComponentId`
   * `SensorId`
