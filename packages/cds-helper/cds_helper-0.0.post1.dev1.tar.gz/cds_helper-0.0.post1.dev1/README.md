# CDS-Helper

Utility to make retrieval of a contiguous set of data files easier.

## Installation

```sh
pip install cds-helper
```

## Using the CLI

### 1. Parameterize a request

Create a `JSON` file describing your desired download.

```json
// cdsrequest.json
{
    "dataset": "reanalysis-era5-single-levels",
    "start_date": "2027-01-01",
    "end_date": "2027-12-31",
    "dataset": "reanalysis",
    "variables": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_dewpoint_temperature",
        "2m_temperature",
        "sea_surface_temperature",
        "total_precipitation",
        "surface_net_solar_radiation",
        "surface_thermal_radiation_downwards",
    ]
}
```

> [!NOTE]
> You can let the cli generate a template `JSON` file for you:
>
> ```sh
> cdshelper template -request ./request.json
> ```

### 2. Execute the request

Pass the path to your `JSON` file to `cdshelper request`

```sh
cdshelper request ./cdsrequest.json
```

## Using the library in your code

```python
import asyncio
import datetime
import logging
import pathlib
import sys

from cds_helper.core import (
    CdsDataRequest,
    download_monthly_data,
)


async def retrieval_demo(log: logging.Logger) -> None:
    """Demo usage of the method `download_monthly_data` from CDS helper."""
    # Create a CdsDataRequest defining the parameters for retrieval.
    request = CdsDataRequest(
        "reanalysis-era5-single-levels",
        datetime(2017, 1, 1),
        datetime(2017, 2, 1),
        "reanalysis",
        variables=[
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_dewpoint_temperature",
            "2m_temperature",
            "sea_surface_temperature",
            "total_precipitation",
            "surface_net_solar_radiation",
            "surface_thermal_radiation_downwards",
        ],
    )

    # Create a mapping from the paths in the archive to the desired
    # local paths. Add a string template `{0}` to allow cds-helper to
    # rename output files based on the request parameters.
    file_map = {
        "data_stream-oper_stepType-instant.nc": "{0}_inst.nc",
        "data_stream-oper_stepType-accum.nc": "{0}_inst.nc",
    }

    # Specify the directory where output will be stored.
    output_to = pathlib.Path("~/datasets").expanduser()

    # Trigger retrieval.
    download_monthly_data(request, file_map, output_to)


async def main(_args_list: list[str]) -> int:
    """Execute the cds-helper CLI."""
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()

    retrieval_demo(log)


if __name__ == "__main__":
    rc = asyncio.run(main(sys.argv[1:]))
    sys.exit(rc)

```
