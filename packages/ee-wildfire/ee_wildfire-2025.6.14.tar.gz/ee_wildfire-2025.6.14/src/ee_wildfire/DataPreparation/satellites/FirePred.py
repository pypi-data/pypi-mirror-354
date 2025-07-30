import datetime

import math

# Google didn't provide documentation stub. This is to fix LSP yelling
from ee import Image #type: ignore
from ee import ImageCollection #type: ignore
from ee import FeatureCollection #type: ignore
from ee import Filter #type: ignore
from ee import Reducer #type: ignore
from ee import Number #type: ignore
from ee import String #type: ignore
from ee import Terrain #type: ignore
from ee import Geometry

from ee_wildfire.UserInterface import ConsoleUI #type: ignore


class FirePred:
    def __init__(self):
        """_summary_ This class describes which data to extract how from Google Earth Engine. 
        The init defines the different source data products to use. 
        """
        self.name = "FirePred"
        # Digital elevation model
        self.srtm = Image("USGS/SRTMGL1_003")
        # Land cover
        self.landcover = ImageCollection("MODIS/061/MCD12Q1")
        # Weather data (GRIDMET)
        self.weather = ImageCollection("IDAHO_EPSCOR/GRIDMET")
        # Weather forecast data (GFS)
        self.weather_forecast = ImageCollection('NOAA/GFS0P25')
        # Drought data (GRIDMET)
        self.drought = ImageCollection("GRIDMET/DROUGHT")
        # VIIRS surface reflectance, needed updating to current dataset
        self.viirs = ImageCollection('NASA/VIIRS/002/VNP09GA')
        # VIIRS active fire product
        self.viirs_af = FeatureCollection('projects/grand-drive-285514/assets/afall')
        # self.viirs_af = ee.FeatureCollection('projects/ee-earthdata/assets/viirs_J1V_af_points') # if this doesnt work try the SUOMI points
        # self.viirs_af = ee.FeatureCollection('projects/ee-earthdata/assets/fire_archive_SV-C2_574505') # This is the historical archive (02-01-2012 to end of 2024)
        # VIIRS vegetation index, needed updating to new dataset
        self.viirs_veg_idx = ImageCollection("NASA/VIIRS/002/VNP13A1")
        ConsoleUI.debug(self)

    def __repr__(self) -> str:
        output_str = "FirePred.py\n"
        for key, value in self.__dict__.items():
            output_str += f"{key} {value}\n"
        return(output_str)

    def compute_daily_features(self, start_time:str, end_time:str, geometry:Geometry) -> ImageCollection:
        """_summary_ Compute the daily features in Google Earth Engine.

        Args:
            start_time (str): _description_
            end_time (str): _description_
            geometry (ee.Geometry): _description_

        Returns:
            ee.ImageCollection: _description_ ImageCollection containing one image, 
            with all desired features for the given day, inside the given geometry.
        """


        # Time objects we need later. We add "000" to timestamps, because GEE has timestamps with miliseconds,
        # but datetime doesn't by default
        today_string = start_time[:-6].replace("-", "")
        today = datetime.datetime.strptime(start_time[:-6], '%Y-%m-%d')
        today_timestamp = int(datetime.datetime.timestamp(today)) * 1000

        today = datetime.datetime.strptime(start_time[:-6], '%Y-%m-%d')
        tomorrow = today + datetime.timedelta(days=1)
        today_string = start_time[:-6].replace("-", "")
        
        # Convert to Unix millisecond timestamps for VIIRS AF filtering
        start_timestamp = int(today.timestamp()) * 1000
        end_timestamp = int(tomorrow.timestamp()) * 1000
        today_timestamp = start_timestamp  # For drought data

        # Weather Data
        # Median is used to turn ee.ImageCollection into a single ee.Image.
        # Each ImageCollection should only contain a single image at this point.
        weather = self.weather.filterDate(start_time, end_time).filterBounds(geometry)
        precipitation = weather.select('pr').median().rename("total precipitation")
        wind_direction = weather.select('th').median().rename("wind direction")
        temperature_min = weather.select('tmmn').median().rename("minimum temperature")
        temperature_max = weather.select('tmmx').median().rename("maximum temperature")
        energy_release_component = weather.select('erc').median().rename("energy release component")
        specific_humidity = weather.select('sph').median().rename("specific humidity")
        wind_velocity = weather.select('vs').median().rename("wind speed")

        # Take forecasts made at midnight (00), and that tell us something about the hours between 01 and 24.
        # Important: The forecasts at 00 contain six features instead of nine, like all others.
        weather_forecast = self.weather_forecast.filter(
            Filter.gte("system:index", today_string + "00F01")).filter(
            Filter.lte("system:index", today_string + "00F24")
        ).filterBounds(geometry)
        forecast_temperature = weather_forecast.select("temperature_2m_above_ground").mean().rename(
            "forecast temperature")
        forecast_specific_humidity = weather_forecast.select("specific_humidity_2m_above_ground").mean().rename(
            "forecast specific humidity")
        forecast_u_wind = weather_forecast.select("u_component_of_wind_10m_above_ground").mean()
        forecast_v_wind = weather_forecast.select("v_component_of_wind_10m_above_ground").mean()

        # Transform from u/v to direction and speed, to align with GRIDMET and DEM data
        forecast_wind_speed = forecast_u_wind.multiply(forecast_u_wind).add(
            forecast_v_wind.multiply(forecast_v_wind)).sqrt().rename("forecast wind speed")
        forecast_wind_direction = forecast_v_wind.divide(forecast_u_wind).atan()
        forecast_wind_direction = forecast_wind_direction.divide(2 * math.pi).multiply(360).rename(
            "forecast wind direction")

        # Rain forecasts were changed: From rain within the one-hour interval to cumulative rain during the day so far
        forecast_rain_change_date = datetime.datetime.strptime("2019-11-07T06:00:00", '%Y-%m-%dT%H:%M:%S')
        forecast_rain = weather_forecast.select("total_precipitation_surface")
        if today <= forecast_rain_change_date:
            forecast_rain = forecast_rain.reduce(Reducer.sum())
        else:
            forecast_rain = forecast_rain.reduce(Reducer.last())
        forecast_rain.rename("forecast total precipitation")
        # Elevation Data
        elevation = self.srtm.select('elevation')
        slope = Terrain.slope(elevation)
        aspect = Terrain.aspect(elevation)

        # Drought Data
        # Only available every fifth day, but we can find the valid entry via time_start and time_end
        drought_index = self.drought \
            .filter(Filter.lte("system:time_start", today_timestamp)) \
            .filter(Filter.gte("system:time_end", today_timestamp)) \
            .select('pdsi').median()
        igbp_land_cover = self.landcover.filterDate(start_time[:4] + '-01-01', start_time[:4] + '-12-31').filterBounds(
            geometry).select('LC_Type1').median()

        # Turn acq_time (String) into acq_hour (int)
        def add_acq_hour(feature):
            acq_time_str = String(feature.get("ACQ_TIME"))
            acq_time_int = Number.parse(acq_time_str)
            return feature.set({"acq_hour": acq_time_int})

        # VIIRS IMG and AF product
        viirs_img = self.viirs.filterDate(start_time, end_time).filterBounds(geometry).select(
            ['M11', 'I2', 'I1']).median()
        viirs_veg_idc = self.viirs_veg_idx.filterDate((
                datetime.datetime.strptime(end_time[:-6], '%Y-%m-%d') + datetime.timedelta(-15)).strftime(
            '%Y-%m-%d'), end_time).filterBounds(geometry).select(['NDVI', 'EVI2']).reduce(
            Reducer.last())

        # Updated VIIRS AF filtering to use Unix millisecond timestamps
        viirs_af_img = self.viirs_af.map(add_acq_hour).filterBounds(geometry) \
            .filter(Filter.gte('ACQ_DATE', start_timestamp)) \
            .filter(Filter.lt('ACQ_DATE', end_timestamp)) \
            .filter(Filter.neq('CONFIDENCE', 'l')).map(self.get_buffer) \
            .reduceToImage(['acq_hour'], Reducer.last()) \
            .rename(['active fire'])

        return ImageCollection(Image(
            [viirs_img, viirs_veg_idc, precipitation, wind_velocity, wind_direction, temperature_min, temperature_max,
             energy_release_component, specific_humidity, slope, aspect,
             elevation, drought_index, igbp_land_cover,
             forecast_rain, forecast_wind_speed, forecast_wind_direction, forecast_temperature,
             forecast_specific_humidity,
             viirs_af_img]))

    def get_buffer(self, feature):
        return feature.buffer(375 / 2).bounds()
