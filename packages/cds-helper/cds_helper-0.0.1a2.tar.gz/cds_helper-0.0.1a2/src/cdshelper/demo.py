import asyncio
import logging
import pathlib
import sys
from datetime import datetime

from cdshelper.core.core import (
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
    log.debug(f"Created request {request}")

    # Create a mapping from the paths in the archive to the desired
    # local paths. Add a string template `{0}` to allow cds-helper to
    # rename output files based on the request parameters.
    file_map = {
        "data_stream-oper_stepType-instant.nc": "{0}_inst.nc",
        "data_stream-oper_stepType-accum.nc": "{0}_inst.nc",
    }
    log.debug(f"Created file_map {file_map}")

    # Specify the directory where output will be stored.
    output_to = pathlib.Path("~/datasets").expanduser()
    log.debug(f"Using output path {output_to}")

    # Trigger retrieval.
    download_monthly_data(request, file_map, output_to)
    log.debug(f"Using output path {output_to}")


async def main(_args_list: list[str]) -> int:
    """Execute the cds-helper CLI."""
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()

    try:
        await retrieval_demo(log)
        return 0
    except Exception:
        log.exception("Retrieval demo failed.")

    return 1


if __name__ == "__main__":
    rc = asyncio.run(main(sys.argv[1:]))
    sys.exit(rc)
