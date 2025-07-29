import pyarrow as pa
import pyarrow.compute as pc
from datetime import datetime
from typing import Optional, Union

from EstateEdgePy.src.utils import parse_date
from EstateEdgePy.filters._base_filter_ import BaseFilter


class DateRangeFilter(BaseFilter):
    def __init__(
            self,
            date_column: str,
            start_date: Optional[Union[str, datetime]] = None,
            end_date: Optional[Union[str, datetime]] = None,
    ):
        self.date_column = date_column
        self.start_date = parse_date(start_date)
        self.end_date = parse_date(end_date)

        # Validate date range
        if (self.start_date and self.end_date and
            self.start_date > self.end_date):
            raise ValueError(
                f"Invalid date range: start_date ({self.start_date}) "
                f"cannot be after end_date ({self.end_date})"
            )

    def apply(self, data: pa.Table) -> pa.Table:
        # Check if column exists
        if self.date_column not in data.column_names:
            raise ValueError(
                f"Column '{self.date_column}' not found in data. "
                f"Available columns: {data.column_names}"
            )

        # Return original data if no filtering needed
        if self.start_date is None and self.end_date is None:
            return data

        mask = None
        timestamps = data[self.date_column].cast("timestamp[ms]")

        if self.start_date:
            start_mask = pc.greater_equal(timestamps, pa.scalar(self.start_date))
            mask = start_mask if mask is None else pc.and_(mask, start_mask)

        if self.end_date:
            end_mask = pc.less_equal(timestamps, pa.scalar(self.end_date))
            mask = end_mask if mask is None else pc.and_(mask, end_mask)

        return data.filter(mask) if mask is not None else data
