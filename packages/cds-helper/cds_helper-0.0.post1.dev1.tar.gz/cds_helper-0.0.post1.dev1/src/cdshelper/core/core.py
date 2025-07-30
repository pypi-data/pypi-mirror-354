"""CDS API - Multi-month Data Retrieval Demo."""

# ruff: noqa: DTZ001
import dataclasses
import pathlib
import typing as t
import zipfile
from datetime import datetime
from tempfile import mkdtemp

import cdsapi


@dataclasses.dataclass
class CdsDataRequest:
    """Data request for a month."""

    dataset: str
    start_date: datetime
    end_date: datetime
    data_type: str
    variables: list[str]
    data_format: str = "netcdf"
    download_format: str = "zip"
    dry_run: bool = False


@dataclasses.dataclass
class CdsMonthlyDataRequest:
    """Monthly data request for the CDS API."""

    year: str
    month: str
    days: list[str]
    hours: list[str]

    request: CdsDataRequest

    def to_body(self) -> dict[str, t.Union[str, list[str]]]:
        """Convert the request to a body suitable for the CDS API."""
        return {
            "product_type": [self.request.data_type],
            "variable": self.request.variables,
            "year": [self.year],
            "month": [self.month],
            "day": self.days,
            "time": self.hours,
            "data_format": self.request.data_format,
            "download_format": self.request.download_format,
        }

    @property
    def base_name(self) -> str:
        """Generate a base name for output files based on request parameters."""
        return f"{self.request.dataset}_{self.year}-{self.month}"


class SourceTargetPathPair(t.NamedTuple):
    """A pair of source and target paths for file mapping."""

    source: pathlib.Path
    target: pathlib.Path


class CdsDatasetDownloader:
    """Client for retrieving data from the Climate Data Store."""

    def __init__(self, dataset: str) -> None:
        """Initialize the data client for a specific dataset."""
        self.dataset = dataset
        self.client = cdsapi.Client()

    def _map_to_paths(
        self,
        extract_to: pathlib.Path,
        output_to: pathlib.Path,
        file_map: dict[str, str],
        base_name: str,
    ) -> list[SourceTargetPathPair]:
        """Map file names from the archive to local paths based on the file map."""
        return [
            SourceTargetPathPair(
                (extract_to / source).resolve(),
                (output_to / target.format(base_name)).resolve(),
            )
            for source, target in file_map.items()
        ]

    def download(
        self,
        request: CdsMonthlyDataRequest,
        file_map: dict[str, str],
        output_to: pathlib.Path,
    ) -> list[pathlib.Path]:
        """Download data for the given request and extract the data.

        :param request: The data request containing dataset, year, month, and days.
        :param file_map: A mapping of archive file paths to local file paths. Maps
        will be used to rename the extracted content if a template location is
        found in the value, e.g. `{"original.nc": "{0}-new-file-name.nc"}`

        :return: A list of paths to the extracted files.
        """
        archive = pathlib.Path(f"./{request.base_name}.zip")
        extract_to = pathlib.Path(mkdtemp())

        if not request.request.dry_run:
            self.client.retrieve(self.dataset, request.to_body(), archive)

        extracted_files: list[pathlib.Path] = []

        local_paths = self._map_to_paths(
            extract_to,
            output_to,
            file_map,
            request.base_name,
        )

        # If all target files have been extracted & renamed, exit early.
        dne = [x for x in local_paths if not x.target.exists()]
        if not dne:
            print(f"{request.base_name} already downloaded, skipping extraction.")
            return [x.target for x in local_paths]

        print(f"extracting {archive}")
        with zipfile.ZipFile(archive, "r") as zip_ref:
            members = file_map.values() if file_map else None
            zip_ref.extractall(extract_to, members)

        for pair in dne:
            pair.source.rename(pair.target)
            extracted_files.append(pair.target)

        archive.unlink()
        print(f"{request.base_name} download complete")
        return extracted_files


def create_monthly_requests(
    request: CdsDataRequest,
) -> t.Iterable[CdsMonthlyDataRequest]:
    """Create request bodies for every month in the given date range."""
    current_date = request.start_date
    end_date = request.end_date

    hours = [f"{str(i).zfill(2)}:00" for i in range(24)]

    while current_date < end_date:
        next_month = datetime(
            current_date.year, current_date.month + 1, current_date.day
        )
        num_days = (next_month - current_date).days
        year = str(current_date.year)
        month = str(current_date.month).zfill(2)
        days = [str(day).zfill(2) for day in range(1, num_days + 1)]

        yield CdsMonthlyDataRequest(year, month, days, hours, request)
        current_date = next_month


def download_monthly_data(
    request: CdsDataRequest,
    file_map: dict[str, str],
    output_to: pathlib.Path,
) -> None:
    """Download monthly data for the specified dataset and date range."""
    client = CdsDatasetDownloader(request.dataset)

    for monthly in create_monthly_requests(request):
        extracted = client.download(monthly, file_map, output_to)
        print("Files extracted:", extracted)
