# projected_solar_wind_data
Write a script that extracts the data on these webpages (ideally not the CSV) to aggregate projected and actual solar and wind generation (MWh) by day for the last 30 days within PJM. Forecasts should be collected from a consistent evaluation time each day for the following day.



https://dataminer2.pjm.com/feed/hourly_solar_power_forecast
https://dataminer2.pjm.com/feed/hourly_wind_power_forecast

The script should output a dictionary structured as follows:

{
  "2000-01-01": {
    "projected": {
      "wind": 500,
      "solar": 300
    },
    "actual": {
      "wind": 515,
      "solar": 297
    }
  },
  "2000-01-02": {
    "projected": {
      "wind": 550,
      "solar": 325
    },
    "actual": {
      "wind": 523,
      "solar": 308
    }
  },
  ...
}

