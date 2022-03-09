from enum import Enum


# See https://confluence.govcloud.dk/pages/viewpage.action?pageId=26476616
class Parameter(Enum):
    TempDry = "temp_dry"
    TempDew = "temp_dew"
    TempMeanPast1h = "temp_mean_past1h"
    TempMaxPast1h = "temp_max_past1h"
    TempMinPast1h = "temp_min_past1h"
    TempMaxPast12h = "temp_max_past12h"
    TempMinPast12h = "temp_min_past12h"
    TempGrass = "temp_grass"
    TempGrassMaxPast1h = "temp_grass_max_past1h"
    TempGrassMeanPast1h = "temp_grass_mean_past1h"
    TempGrassMinPast1h = "temp_grass_min_past1h"
    TempSoil = "temp_soil"
    TempSoilMaxPast1h = "temp_soil_max_past1h"
    TempSoilMeanPast1h = "temp_soil_mean_past1h"
    TempSoilMinPast1h = "temp_soil_min_past1h"
    Humidity = "humidity"
    HumidityPast1h = "humidity_past1h"
    Pressure = "pressure"
    PressureAtSea = "pressure_at_sea"
    WindDir = "wind_dir"
    WindDirPast1h = "wind_dir_past1h"
    WindSpeed = "wind_speed"
    WindSpeedPast1h = "wind_speed_past1h"
    WindGustAlwaysPast1h = "wind_gust_always_past1h"
    WindMax = "wind_max"
    WindMinPast1h = "wind_min_past1h"
    WindMin = "wind_min"
    WindMaxPer10minPast1h = "wind_max_per10min_past1h"
    PrecipPast1h = "precip_past1h"
    PrecipPast10min = "precip_past10min"
    PrecipPast1min = "precip_past1min"
    PrecipPast24h = "precip_past24h"
    PrecipDurPast10min = "precip_dur_past10min"
    PrecipDurPast1h = "precip_dur_past1h"
    SnowDepthMan = "snow_depth_man"
    SnowCoverMan = "snow_cover_man"
    Visibility = "visibility"
    VisibMeanLast10min = "visib_mean_last10min"
    CloudCover = "cloud_cover"
    CloudHeight = "cloud_height"
    Weather = "weather"
    RadiaGlob = "radia_glob"
    RadiaGlobPast1h = "radia_glob_past1h"
    SunLast10minGlob = "sun_last10min_glob"
    SunLast1hGlob = "sun_last1h_glob"
    LeavHumDurPast10min = "leav_hum_dur_past10min"
    LeavHumDurPast1h = "leav_hum_dur_past1h"


# https://confluence.govcloud.dk/pages/viewpage.action?pageId=41717444
class ClimateDataParameter(Enum):
    MeanTemp = "mean_temp"
    MeanDailyMaxTemp = "mean_daily_max_temp"
    MaxTempWDate = "max_temp_w_date"
    MaxTemp_12h = "max_temp_12h"
    NoIceDays = "no_ice_days"
    NoSummerDays = "no_summer_days"
    MeanDailyMinTemp = "mean_daily_min_temp"
    MinTemp = "min_temp"
    MinTemperature_12h = "min_temperature_12h"
    NoColdDays = "no_cold_days"
    NoFrostDays = "no_frost_days"
    NoTropicalNights = "no_tropical_nights"
    AccHeatingDegreeDays_17 = "acc_heating_degree_days_17"
    AccHeatingDegreeDays_19 = "acc_heating_degree_days_19"
    MeanRelativeHum = "mean_relative_hum"
    MaxRelativeHum = "max_relative_hum"
    MinRelativeHum = "min_relative_hum"
    MeanVapourPressure = "mean_vapour_pressure"
    MeanWindSpeed = "mean_wind_speed"
    MaxWindSpeed_10min = "max_wind_speed_10min"
    MaxWindSpeed_3sec = "max_wind_speed_3sec"
    NoWindyDays = "no_windy_days"
    NoStormyDays = "no_stormy_days"
    NoDaysWStorm = "no_days_w_storm"
    NoDaysWHurricane = "no_days_w_hurricane"
    MeanWindDirMin0 = "mean_wind_dir_min0"
    MeanWindDir = "mean_wind_dir"
    MeanPressure = "mean_pressure"
    MaxPressure = "max_pressure"
    MinPressure = "min_pressure"
    BrightSunshine = "bright_sunshine"
    MeanRadiation = "mean_radiation"
    AccPrecip = "acc_precip"
    MaxPrecip_24h = "max_precip_24h"
    AccPrecipPast12h = "acc_precip_past12h"
    NoDaysAccPrecip_01 = "no_days_acc_precip_01"
    NoDaysAccPrecip_1 = "no_days_acc_precip_1"
    NoDaysAccPrecip_10 = "no_days_acc_precip_10"
    AccPrecipPast24h = "acc_precip_past24h"
    MaxPrecip_30m = "max_precip_30m"
    NoDaysSnowCover = "no_days_snow_cover"
    MeanCloudCover = "mean_cloud_cover"
    NoClearDays = "no_clear_days"
    NoCloudyDays = "no_cloudy_days"
    MaxSnowDepth = "max_snow_depth"
    SnowDepth = "snow_depth"
    SnowCover = "snow_cover"
    TempGrass = "temp_grass"
    TempSoil_10 = "temp_soil_10"
    TempSoil_30 = "temp_soil_30"
    LeafMoisture = "leaf_moisture"
    VapourPressureDeficitMean = "vapour_pressure_deficit_mean"
