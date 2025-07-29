"""Intake driver for GFS forecast data from NCAR NOMADS.

This module provides an Intake driver for accessing Global Forecast System (GFS)
forecast data from the NCAR NOMADS server.
"""

import logging
import traceback
from datetime import datetime, time, timezone
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import xarray as xr
from intake.source.base import DataSource, Schema

logger = logging.getLogger(__name__)

# Default GFS data URL (NCAR NOMADS)
DEFAULT_BASE_URL = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"

# Default file pattern for GFS forecast files
DEFAULT_FILE_PATTERN = (
    "{base_url}/gfs.{date:%Y%m%d}/{model_run_time:02d}/"
    "atmos/gfs.t{model_run_time:02d}z.pgrb2.0p25.f{lead_time:03d}"
)


class GFSForecastSource(DataSource):
    """Intake driver for GFS forecast data from NCAR NOMADS.

    This driver provides access to GFS forecast data in GRIB2 format from the
    NCAR NOMADS server. It supports filtering by variable, level, and forecast
    lead time, and returns data as xarray Datasets.

    Parameters
    ----------
    date_str : str or datetime-like
        Forecast initialization date in 'YYYY-MM-DD' format or datetime object
    max_lead_time_fXXX : str, optional
        Maximum forecast lead time as 'fHHH' (e.g., 'f024' for 24 hours)
    base_url : str, optional
        Base URL for the NOMADS server
    model_run_time : str or int, optional
        Model run time in 'HH' format (e.g., '00' or 0 for 00Z run)
    cfgrib_filter_by_keys : dict, optional
        Dictionary of GRIB filter parameters (e.g., {'typeOfLevel': 'surface'})
    metadata : dict, optional
        Additional metadata to include in the source
    """

    name = "gfs_forecast"
    version = "0.1.0"
    container = "xarray"
    partition_access = True

    def __init__(
        self,
        cycle: Union[str, datetime] = "latest",
        max_lead_time: int = 24,
        base_url: str = DEFAULT_BASE_URL,
        cfgrib_filter_by_keys: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(metadata=metadata or {})

        # Parse and validate cycle (date and model run time)
        try:
            if isinstance(cycle, str):
                if cycle.lower() == "latest":
                    # Use current time if 'latest' is specified
                    cycle_dt = datetime.now(timezone.utc)
                    # Round down to the nearest 6-hour cycle (00, 06, 12, 18Z)
                    hour = (cycle_dt.hour // 6) * 6
                    cycle_dt = cycle_dt.replace(
                        hour=hour, minute=0, second=0, microsecond=0
                    )
                    self.date = cycle_dt.date()
                    self.model_run_time = cycle_dt.hour
                    logger.info(
                        f"Using latest cycle: {cycle_dt.isoformat()} ({self.model_run_time:02d}Z)"
                    )
                else:
                    try:
                        cycle_dt = datetime.fromisoformat(cycle)
                    except ValueError:
                        # Fall back to pandas for more flexible parsing
                        cycle_dt = pd.to_datetime(cycle)
                    self.date = cycle_dt.date()
                    self.model_run_time = cycle_dt.hour
            else:
                cycle_dt = pd.to_datetime(cycle)
                self.date = cycle_dt.date()
                self.model_run_time = cycle_dt.hour

            # Validate model run time is valid
            if not (0 <= self.model_run_time <= 23):
                raise ValueError("Cycle hour must be between 0 and 23")

        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Invalid cycle format: {cycle}. Expected ISO format "
                f"(YYYY-MM-DDTHH:MM:SS), 'latest', or datetime object"
            ) from e

        # Validate max_lead_time
        try:
            self.max_lead_time = int(max_lead_time)
            if self.max_lead_time <= 0:
                raise ValueError("max_lead_time must be a positive integer")
            if (
                self.max_lead_time > 384
            ):  # Maximum GFS forecast length is typically 384 hours
                logger.warning(
                    f"max_lead_time={max_lead_time} is greater than typical GFS maximum of 384 hours"
                )
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Invalid max_lead_time: {max_lead_time}. Expected positive " f"integer"
            ) from e

        self.base_url = base_url.rstrip("/")
        self.cfgrib_filter_by_keys = cfgrib_filter_by_keys or {}
        self._ds = None
        self._urls = None

        # Create the cycle datetime for metadata
        cycle_datetime = datetime.combine(self.date, time(hour=self.model_run_time))

        # Update metadata
        self.metadata.update(
            {
                "cycle": cycle_datetime.isoformat(),
                "date": self.date.isoformat(),
                "max_lead_time": self.max_lead_time,
                "model_run_time": f"{self.model_run_time:02d}Z",
                "base_url": self.base_url,
                "cfgrib_filter_by_keys": self.cfgrib_filter_by_keys,
                **kwargs,
            }
        )

        logger.info(
            f"Initialized GFS source for cycle: {cycle_datetime.isoformat()} "
            f"with max_lead_time: {self.max_lead_time}"
        )

    def _build_urls(self) -> List[str]:
        """Build URLs for all forecast lead times up to max_lead_time."""
        if self._urls is not None:
            return self._urls

        urls = []
        date_str = self.date.strftime("%Y%m%d")
        model_run_time_str = f"{self.model_run_time:02d}"

        logger.info(
            f"Building URLs for max_lead_time={self.max_lead_time} (f{self.max_lead_time:03d})"
        )

        # GFS files are available in 3-hour increments up to 120 hours,
        # then 6-hour increments up to 240 hours, and 12-hour increments beyond that
        for lead_time in range(0, min(self.max_lead_time, 120) + 1, 3):
            url = (
                f"{self.base_url}/gfs.{date_str}/{model_run_time_str}/"
                f"atmos/gfs.t{model_run_time_str}z.pgrb2.0p25.f{lead_time:03d}"
            )
            urls.append(url)
            logger.debug(f"Added URL for lead_time={lead_time}: {url}")

        if self.max_lead_time > 120:
            for lead_time in range(123, min(self.max_lead_time, 240) + 1, 3):
                url = (
                    f"{self.base_url}/gfs.{date_str}/{model_run_time_str}/"
                    f"atmos/gfs.t{model_run_time_str}z.pgrb2.0p25.f{lead_time:03d}"
                )
                urls.append(url)
                logger.debug(f"Added URL for lead_time={lead_time}: {url}")

        if self.max_lead_time > 240:
            for lead_time in range(246, self.max_lead_time + 1, 6):
                url = (
                    f"{self.base_url}/gfs.{date_str}/{model_run_time_str}/"
                    f"atmos/gfs.t{model_run_time_str}z.pgrb2.0p25.f{lead_time:03d}"
                )
                urls.append(url)
                logger.debug(f"Added URL for lead_time={lead_time}: {url}")

        # Add .idx file for better performance with cfgrib
        # urls = [f"{url}.idx" for url in urls] + urls

        self._urls = urls
        logger.info(
            f"Generated {len(urls)} URLs for GFS data from {date_str} {model_run_time_str}Z"
        )
        if urls:
            logger.info(f"First URL: {urls[0]}")
            if len(urls) > 1:
                logger.info(f"Last URL: {urls[-1]}")
                logger.info(f"All URLs: {urls}")
        else:
            logger.warning("No URLs generated - check date and model run time")

        return urls

    def _get_schema(self) -> Schema:
        """Get schema for the data source."""
        if self._schema is not None:
            return self._schema

        self._build_urls()

        if not self._urls:
            raise ValueError("No valid URLs found for the specified parameters")

        # Try to open the first file to get the schema
        try:
            # Import required modules
            import os
            import shutil
            import tempfile
            import urllib.request

            url = self._urls[0]
            logger.info(f"Downloading file for schema: {url}")

            # Create a temporary directory for the download
            temp_dir = tempfile.mkdtemp(prefix="gfs_intake_")
            try:
                # Download the file with a .grib2 extension
                temp_file = os.path.join(temp_dir, "temp.grib2")
                logger.info(f"Downloading to temporary file: {temp_file}")

                # Download with a timeout
                try:
                    with (
                        urllib.request.urlopen(url, timeout=30) as response,
                        open(temp_file, "wb") as out_file,
                    ):
                        shutil.copyfileobj(response, out_file)
                except Exception as e:
                    raise IOError(f"Failed to download {url}: {e}")

                # Check if the file was downloaded successfully
                if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                    raise IOError(
                        f"Downloaded file is empty or does not exist: {temp_file}"
                    )

                logger.info(
                    f"Successfully downloaded {os.path.getsize(temp_file)} bytes"
                )

                # Try to open with cfgrib
                backend_kwargs = {
                    "indexpath": "",
                    "errors": "raise",  # Raise exceptions to see actual errors
                    "filter_by_keys": self.cfgrib_filter_by_keys or {},
                }

                logger.info(f"Opening GRIB file with cfgrib backend: {temp_file}")
                logger.info(f"Using backend kwargs: {backend_kwargs}")

                # Open the dataset
                try:
                    ds = xr.open_dataset(
                        temp_file, engine="cfgrib", backend_kwargs=backend_kwargs
                    )

                    # Log basic info about the dataset
                    logger.info(
                        f"Successfully opened dataset with {len(ds.variables)} "
                        f"variables"
                    )
                    logger.info(f"Dataset variables: {list(ds.variables.keys())}")
                    logger.info(f"Dataset dimensions: {dict(ds.sizes)}")

                    # Convert to schema
                    shape = {k: v for k, v in ds.sizes.items()}
                    dtype = {k: str(v.dtype) for k, v in ds.variables.items()}

                    self._schema = Schema(
                        datashape=None,
                        shape=tuple(shape.values()) if shape else None,
                        dtype=dtype,
                        npartitions=len(self._urls),
                        extra_metadata={
                            "variables": list(ds.data_vars.keys()),
                            "coords": list(ds.coords.keys()),
                            "dims": dict(ds.sizes),
                        },
                    )

                    # Store the dataset if it's small enough
                    if sum(shape.values()) < 1e6:  # Arbitrary threshold
                        self._ds = ds

                    return self._schema

                except Exception as e:
                    logger.error(f"Error opening GRIB file with cfgrib: {e}")
                    logger.debug(f"Traceback: {traceback.format_exc()}")
                    raise

            finally:
                # Clean up the temporary directory
                try:
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                        logger.debug(f"Removed temporary directory: {temp_dir}")
                except Exception as e:
                    logger.warning(
                        f"Could not remove temporary directory {temp_dir}: {e}"
                    )

        except Exception as e:
            logger.error(f"Error getting schema: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")

            # Return an empty schema if we can't determine it
            self._schema = Schema(
                datashape=None,
                shape=None,
                npartitions=(
                    len(self._urls) if hasattr(self, "_urls") and self._urls else 0
                ),
                extra_metadata={
                    "error": str(e),
                    "urls": (
                        self._urls[:5] if hasattr(self, "_urls") and self._urls else []
                    ),
                },
            )

        return self._schema

    def _get_partition(self, i: int) -> xr.Dataset:
        """Get one partition from the dataset.

        Parameters
        ----------
        i : int
            The partition number to read.

        Returns
        -------
        xarray.Dataset
            The dataset for the specified partition.
        """
        if self._urls is None:
            self._build_urls()

        if i >= len(self._urls):
            raise IndexError(f"Partition {i} is out of range (0-{len(self._urls)-1})")

        url = self._urls[i]
        logger.info(f"Reading data from {url}")

        try:
            # Create a temporary file to download the GRIB file
            import os
            import tempfile
            import urllib.request

            with tempfile.NamedTemporaryFile(suffix=".grib2", delete=False) as tmp_file:
                tmp_path = tmp_file.name

            # Download the file
            logger.info(f"Downloading GRIB file to temporary location: {tmp_path}")
            urllib.request.urlretrieve(url, tmp_path)

            # Check if file was downloaded successfully
            if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
                raise IOError(f"Failed to download file from {url}")

            # Open with cfgrib engine and specified filters
            logger.info(f"Opening GRIB file with cfgrib: {tmp_path}")
            backend_kwargs = {
                "indexpath": "",
                "errors": "raise",  # Change to 'raise' to see actual errors
                "filter_by_keys": self.cfgrib_filter_by_keys,
            }

            logger.info(f"Using backend kwargs: {backend_kwargs}")
            logger.info(f"Filter by keys details:")
            for key, value in self.cfgrib_filter_by_keys.items():
                logger.info(f"  {key}: {value}")

            # Try to open the dataset
            try:
                ds = xr.open_dataset(
                    tmp_path, engine="cfgrib", backend_kwargs=backend_kwargs
                )

                # Check if we got any data
                if not ds.variables:
                    logger.warning(f"No variables found in the dataset from {url}")
                else:
                    logger.info(
                        f"Successfully read dataset with variables: {list(ds.variables.keys())}"
                    )

                # Log detailed information about dimensions and coordinates
                logger.info(f"Dataset dimensions: {dict(ds.sizes)}")
                if "time" in ds.coords:
                    logger.info(f"Time values: {ds.time.values}")
                if "step" in ds.coords:
                    logger.info(f"Step values: {ds.step.values}")

                # Add URL as an attribute for reference
                ds.attrs["source_url"] = url
                ds.attrs["lead_time"] = url.split(".")[
                    -1
                ]  # Extract the forecast hour (f000, f003, etc.)

                # Actually load all data into memory to avoid file access issues
                logger.info(f"Loading data into memory from {tmp_path}")
                ds = ds.load()

                # Now we can safely delete the temporary file since data is loaded
                try:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                        logger.debug(f"Removed temporary file: {tmp_path}")
                except Exception as e:
                    logger.warning(f"Could not remove temporary file {tmp_path}: {e}")

                return ds

            except Exception as e:
                logger.error(f"Error opening dataset with cfgrib: {e}")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                # Clean up in case of error
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                raise

        except Exception as e:
            logger.error(f"Error reading data from {url}: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise

    def read(self) -> xr.Dataset:
        """Load entire dataset into memory and return as xarray.Dataset"""
        if self._ds is not None:
            return self._ds

        if self._urls is None:
            self._build_urls()

        if not self._urls:
            logger.warning("No URLs available to read data from")
            return xr.Dataset()

        try:
            logger.info(f"Reading {len(self._urls)} partitions...")
            # Read all partitions and combine
            datasets = []
            for i, url in enumerate(self._urls):
                try:
                    logger.info(f"Reading partition {i+1}/{len(self._urls)} from {url}")
                    ds = self._get_partition(i)
                    if ds is not None and len(ds.variables) > 0:
                        logger.info(
                            f"Successfully read partition {i+1} with variables: {list(ds.variables.keys())}"
                        )
                        datasets.append(ds)
                    else:
                        logger.warning(f"No data in partition {i+1}")
                except Exception as e:
                    logger.error(f"Error reading partition {i+1}: {e}")
                    logger.debug(f"Traceback: {traceback.format_exc()}")
                    # Continue with other partitions even if one fails
                    continue

            if not datasets:
                logger.warning("No data was read from any partition")
                return xr.Dataset()

            logger.info(f"Combining {len(datasets)} partitions...")
            # Combine datasets along the time dimension if it exists
            try:
                if len(datasets) > 1:
                    if "time" in datasets[0].dims:
                        logger.info("Concatenating datasets along time dimension")
                        self._ds = xr.concat(datasets, dim="time")
                    elif "step" in datasets[0].coords:
                        # If no time dimension but step coordinate exists, try to create a new dimension
                        logger.info("Trying to combine datasets along step coordinate")
                        try:
                            # Log each dataset's step value for debugging
                            for i, ds in enumerate(datasets):
                                logger.info(f"Dataset {i} step value: {ds.step.values}")

                            # Create a new dataset that includes step as a dimension
                            # First, ensure the step coordinate values are all different
                            step_values = [ds.step.values.item() for ds in datasets]
                            if len(set(step_values)) != len(step_values):
                                logger.warning(
                                    "Duplicate step values found, cannot combine"
                                )
                                self._ds = datasets[0]
                            else:
                                # Convert step from coordinate to dimension
                                new_datasets = []
                                for ds in datasets:
                                    # Expand step from scalar coordinate to 1-element dimension
                                    ds = ds.expand_dims("step")
                                    new_datasets.append(ds)

                                # Now concat these datasets along the step dimension
                                combined = xr.concat(new_datasets, dim="step")
                                logger.info(
                                    f"Successfully combined datasets along step dimension: {combined.step.values}"
                                )
                                self._ds = combined
                        except Exception as e:
                            logger.error(f"Error combining along step: {e}")
                            logger.debug(f"Traceback: {traceback.format_exc()}")
                            logger.info(
                                "Using only the first dataset due to combination error"
                            )
                            self._ds = datasets[0]
                    else:
                        logger.info(
                            "Using single dataset (no time or step concatenation possible)"
                        )
                        self._ds = datasets[0]
                else:
                    logger.info("Using single dataset (only one available)")
                    self._ds = datasets[0]

                # Log some basic info about the combined dataset
                if hasattr(self._ds, "variables") and self._ds.variables:
                    logger.info(
                        f"Combined dataset has {len(self._ds.variables)} " f"variables"
                    )
                    logger.info(f"Dataset dimensions: {dict(self._ds.sizes)}")

                    # Log time range if time dimension exists
                    if (
                        "time" in self._ds.sizes
                        and hasattr(self._ds, "time")
                        and len(self._ds.time) > 0
                    ):
                        logger.info(
                            f"Time range: {self._ds.time.values.min()} to {self._ds.time.values.max()}"
                        )

                return self._ds

            except Exception as e:
                logger.error(f"Error combining datasets: {e}")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                # Return the first dataset if concatenation fails
                if datasets:
                    logger.info("Returning first dataset due to concatenation error")
                    return datasets[0]
                return xr.Dataset()

        except Exception as e:
            logger.error(f"Error reading dataset: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise

    def to_dask(self):
        """Return a dask array for this data source."""
        return self.read().to_dask()

    def close(self):
        """Close any open files or resources."""
        if self._ds is not None:
            if hasattr(self._ds, "close"):
                self._ds.close()
            self._ds = None
        self._urls = None
        self._schema = None


# Driver registration is now handled in __init__.py to avoid duplicate registrations
