from .magma_seismic import MagmaSeismic
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
from obspy.clients.earthworm import Client
from obspy import UTCDateTime
from typing import Self


class Download(MagmaSeismic):
    host = '172.16.1.220'
    port = 16032
    timeout = 5

    def __init__(self, station: str, channel: str, start_date: str, end_date: str, channel_type: str = 'D',
                 network: str = 'VG', location: str = '00', verbose: bool = False,
                 output_directory: str = None, overwrite: bool = False):
        super().__init__(station, channel, channel_type, network, location, verbose)

        self.start_date_str = start_date
        self.end_date_str = end_date
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

        self.date_range = pd.date_range(start=self.start_date, end=self.end_date, freq='d')

        if output_directory is None:
            output_directory = os.getcwd()
        self.output_directory = os.path.join(output_directory, 'output')
        os.makedirs(self.output_directory, exist_ok=True)

        self.download_directory = os.path.join(self.output_directory, 'download')
        os.makedirs(self.download_directory, exist_ok=True)

        self.overwrite = overwrite

        self.client = Client(
            host='172.16.1.220',
            port=16032,
            timeout=5
        )

        self.failed = []
        self.success = []

        if verbose:
            print('=' * 50)
            print('Station: ' + self.station)
            print('Channel: ' + self.channel)
            print('Network: ' + self.network)
            print('Location: ' + self.location)
            print('=' * 50)
            print('Start date: ' + self.start_date_str)
            print('End date: ' + self.end_date_str)
            print('Output directory: ' + self.output_directory)
            print('Download directory: ' + self.download_directory)
            print('Overwrite file: ' + str(self.overwrite))
            print('=' * 50)
            print('Client host: ' + self.host)
            print('Client port: ' + str(self.port))
            print('Timeout: ' + str(self.timeout))
            print('=' * 50)

    @staticmethod
    def _hours(hour_ranges: pd.DatetimeIndex, period: int) -> list[dict]:
        """Get hours range list

        Args:
            hour_ranges: pd.DatetimeIndex
            period: int

        Returns:
            list[dict]: List of dict with 'index','start_hour' and 'end_hour'
        """
        hours = []
        len_hours: int = len(str(len(hour_ranges)))
        for index, start_hour in enumerate(list(hour_ranges)):
            end_hour = start_hour + timedelta(minutes=period) - timedelta(milliseconds=1)
            hours.append({
                'index': str(index).zfill(len_hours),
                'start_hour': UTCDateTime(start_hour),
                'end_hour': UTCDateTime(end_hour),
            })
        return hours

    def set_client(self, host: str = '172.16.1.220', port: int = 16032, timeout: int = 5) -> Self:
        """Set Winston Client.

        Args:
            host (str): Winston host
            port (int): Winston port
            timeout (int): Winston timeout

        Returns:
            Self
        """
        self.client = Client(
            host=host,
            port=port,
            timeout=timeout
        )

        if self.verbose:
            print(f'ℹ️ Client using {host}:{port} with timeout {timeout}')

        return self

    def _idds(self, date: datetime, period: int, use_merge: bool = False) -> None:
        """Private method to download IDDS

        Args:
            date (datetime): Date to download
            period (int): Period to download
            use_merge (bool, optional): Whether to use merged traces. Defaults to False.

        Returns:
            None
        """
        network = self.network
        station = self.station
        channel = self.channel
        location = self.location
        channel_type = self.channel_type

        year = date.year
        julian_day = date.strftime('%j')

        directory: str = os.path.join(self.download_directory, 'idds')
        os.makedirs(directory, exist_ok=True)

        idds_directory: str = os.path.join(directory, str(year), network, station,
                                           f'{channel}.{channel_type}', julian_day)
        os.makedirs(idds_directory, exist_ok=True)

        start_date_str = date.strftime('%Y-%m-%d')

        hour_ranges = pd.date_range(start=date, end=date, freq=f'{str(period)}min')
        for hour in Download._hours(hour_ranges, period):
            hour_index = hour['index']
            start_hour = hour['start_hour']
            end_hour = hour['end_hour']
            start_hour_str = hour['start_hour'].strftime('%H:%M:%S')
            end_hour_str = hour['end_hour'].strftime('%H:%M:%S')
            nslc: str = f'{network}.{station}.{location}.{channel}.{channel_type}.{year}.{julian_day}.{hour_index}'
            mseed_path: str = os.path.join(idds_directory, nslc)

            info = {
                'nslc': self.nslc,
                'date': start_date_str,
                'start_time': start_hour_str,
                'end_time': end_hour_str,
                'filename': mseed_path,
                'error': None
            }

            if os.path.isfile(mseed_path) and self.overwrite is False:
                print(f'ℹ️ {start_date_str} {start_hour_str} to {end_hour_str} exists. Skipping')
                print(f'🗃️ {mseed_path}')
                self.success.append(info)
                continue

            # Downloading miniseed
            try:
                if self.verbose:
                    print(f'⌛ {start_date_str} {start_hour_str} to {end_hour_str} :: Starting download')
                stream = self.client.get_waveforms(
                    network=network, station=station, location=location,
                    channel=channel, starttime=start_hour, endtime=end_hour)

                if len(stream) == 0:
                    info['error'] = 'Data not found in server'
                    self.failed.append(info)
                    print(f'⚠️ {start_date_str} {start_hour_str} to {end_hour_str} :: Data not found in server')
                    continue

                if self.verbose:
                    print(f'✅ {start_date_str} {start_hour_str} to {end_hour_str} :: Download completed')
            except Exception as e:
                info['error'] = f'Error downloading. {e}'
                self.failed.append(info)
                print(f'❌ {start_date_str} {start_hour_str} to {end_hour_str} :: Error downloading {nslc}\n{e}')
                continue

            # Writing miniseed
            try:
                for trace in stream:
                    trace.data = np.where(trace.data == -2 ** 31, 0, trace.data)
                    trace.data = trace.data.astype(np.int32)

                if use_merge:
                    try:
                        stream.merge(fill_value=0)
                        if self.verbose:
                            print(
                                f'🧲 {start_date_str} {start_hour_str} to {end_hour_str} :: '
                                f'Merged {len(stream)} traces.')
                    except Exception as e:
                        info['error'] = f'Merging error. {e}'
                        self.failed.append(info)
                        if self.verbose:
                            print(f'⚠️ {start_date_str} {start_hour_str} to {end_hour_str} :: '
                                  f'Merging error. Continue without merging. {e}')
                        continue

                stream.write(mseed_path, format='MSEED')
                self.success.append(info)
                print(f'🗃️ {start_date_str} {start_hour_str} to {end_hour_str} saved to :: {mseed_path}')
            except Exception as e:
                info['error'] = f'Error writing trace. {e}'
                self.failed.append(info)
                print(f'❌ Error writing {mseed_path} :: {start_hour_str} to {end_hour_str}\n{e}')
                continue

        return None

    def to_idds(self, period: int = 60, use_merge: bool = False) -> None:
        """Download to IDDS directory.

        Args:
            period (int, optional): Download period in minutes. Defaults to 60 minutes.
            use_merge (bool, optional): Whether to merged traces. Defaults to False.

        Returns:
            None
        """
        assert 0 < period <= 60, ValueError(f'❌ Period must be between 1 to 60 minutes. '
                                            f'Your value is {period} minutes')
        for _date in self.date_range:
            self._idds(_date, period=period, use_merge=use_merge)

        self.print_results()
        return None

    def _sds(self, date: datetime, use_merge: bool = False, chunking: int = None) -> None:
        network = self.network
        station = self.station
        channel = self.channel
        location = self.location
        channel_type = self.channel_type
        year = date.year
        julian_day = date.strftime('%j')

        start_date_str = date.strftime('%Y-%m-%d')
        end_hour = date + timedelta(minutes=60 * 24) - timedelta(milliseconds=1)

        sds_dir = os.path.join(self.download_directory, 'sds', str(year), network, station, f'{channel}.{channel_type}')
        os.makedirs(sds_dir, exist_ok=True)

        filename = f'{network}.{station}.{location}.{channel}.{channel_type}.{year}.{julian_day}'
        filepath = os.path.join(sds_dir, filename)

        info = {
            'nslc': self.nslc,
            'date': start_date_str,
            'start_time': date.strftime('%H:%M:%S'),
            'end_time': end_hour.strftime('%H:%M:%S'),
            'filepath': filepath,
            'error': None
        }

        if os.path.isfile(filepath) and self.overwrite is False:
            print(f'ℹ️ {start_date_str} - {self.nslc} exists. Skipping')
            print(f'🗃️ {filepath}')
            self.success.append(info)
            return None

        tmp_dir = os.path.join(sds_dir, '.tmp')
        if chunking is not None:
            os.makedirs(tmp_dir, exist_ok=True)

        try:
            if self.verbose:
                print(f'⌛ {start_date_str} - {self.nslc} :: Starting download')
                if chunking is not None:
                    print(f'🔢 {start_date_str} - {self.nslc} :: Using {chunking} minutes of chunking')

            stream = self.client.get_waveforms(
                network=network, station=station, location=location,
                channel=channel, starttime=UTCDateTime(date), endtime=UTCDateTime(end_hour))

            if len(stream) == 0:
                info['error'] = 'Data not found in server'
                self.failed.append(info)
                print(f'⚠️ {start_date_str} - {self.nslc} :: Data not found in server')
        except Exception as e:
            info['error'] = f'Error downloading. {e}'
            self.failed.append(info)
            print(f'❌ {start_date_str} - {self.nslc} :: Error downloading\n{e}')
            return None

        if len(stream) > 0:
            try:
                for trace in stream:
                    trace.data = np.where(trace.data == -2 ** 31, 0, trace.data)
                    trace.data = trace.data.astype(np.int32)

                if use_merge:
                    try:
                        stream.merge(fill_value=0)
                        if self.verbose:
                            print(
                                f'🧲 {start_date_str} - {self.nslc} :: Merged {len(stream)} traces.')
                    except Exception as e:
                        info['error'] = f'Merging error. {e}'
                        self.failed.append(info)
                        if self.verbose:
                            print(f'⚠️ {start_date_str} - {self.nslc} :: Continue without merging. {e}')

                stream.write(filepath, format='MSEED')
                self.success.append(info)
                print(f'🗃️ {start_date_str} - {self.nslc} saved to :: {filepath}')
            except Exception as e:
                info['error'] = f'Error writing trace. {e}'
                self.failed.append(info)
                print(f'❌ {start_date_str} Error writing {filepath} :: {e}')
        return None

    def to_sds(self, use_merge: bool = False, chunks_minutes: int = None) -> None:
        """Download to SDS directory.

        Args:
            use_merge (bool, optional): Whether to merged traces. Defaults to False.
            chunks_minutes (int, optional): How many minutes of chunking. Defaults to None.

        Returns:
            None
        """
        for _date in self.date_range:
            self._sds(_date, use_merge=use_merge, chunking=chunks_minutes)

        self.print_results()
        return None

    def print_results(self) -> None:
        """Print results to console.

        Returns:
            None
        """
        print(f'=' * 75)
        if len(self.failed) > 0:
            print(f'⚠️ Failed to download {len(self.failed)} traces')
        print(f'✅ Download completed for {self.nslc} :: {self.start_date_str} to {self.end_date_str}')
        print(f'=' * 75)
        return None
