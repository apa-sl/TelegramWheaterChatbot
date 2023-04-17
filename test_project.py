import pytest
from project import geolocate, trim_weather_forcast_to_a_day, get_weather_forecast

@pytest.fixture
def example_forecast_data():
    # data for Gdynia between 2023-04-06 till 2023-04-12
    return {'latitude': 54.52, 'longitude': 18.539999, 'generationtime_ms': 1.0519027709960938, 'utc_offset_seconds': 7200, 'timezone': 'Europe/Warsaw', 'timezone_abbreviation': 'CEST', 'elevation': 17.0, 'daily_units': {'time': 'iso8601', 'temperature_2m_max': '°C', 'temperature_2m_min': '°C', 'apparent_temperature_max': '°C', 'apparent_temperature_min': '°C', 'sunrise': 'iso8601', 'sunset': 'iso8601', 'precipitation_probability_max': '%', 'precipitation_sum': 'mm', 'windspeed_10m_max': 'km/h'}, 'daily': {'time': ['2023-04-06', '2023-04-07', '2023-04-08', '2023-04-09', '2023-04-10', '2023-04-11', '2023-04-12'], 'temperature_2m_max': [3.2, 7.3, 8.6, 7.3, 8.7, 10.3, 9.7], 'temperature_2m_min': [0.0, 3.1, 4.4, 4.4, 3.4, 3.8, 5.8], 'apparent_temperature_max': [-0.6, 3.7, 6.7, 4.9, 6.3, 8.2, 7.8], 'apparent_temperature_min': [-2.9, -0.4, 2.0, 2.2, 0.8, 1.8, 4.0], 'sunrise': ['2023-04-06T06:04', '2023-04-07T06:01', '2023-04-08T05:59', '2023-04-09T05:56', '2023-04-10T05:54', '2023-04-11T05:51', '2023-04-12T05:49'], 'sunset': ['2023-04-06T19:32', '2023-04-07T19:34', '2023-04-08T19:36', '2023-04-09T19:38', '2023-04-10T19:40', '2023-04-11T19:42', '2023-04-12T19:43'], 'precipitation_probability_max': [0, 55, 45, 23, 6, 48, 29], 'precipitation_sum': [0.0, 0.0, 0.1, 0.1, 0.0, 4.8, 7.5], 'windspeed_10m_max': [13.4, 13.7, 9.3, 8.9, 10.0, 11.2, 9.4]}}


def test_geolocate():
    expected_response1 = {'name': 'Gdynia', 'local_names': {'zh': '格丁尼亚', 'hu': 'Gdynia', 'mk': 'Гдиња', 'de': 'Gdingen', 'el': 'Γδύνια', 'lt': 'Gdynė', 'ru': 'Гдыня', 'cs': 'Gdyně', 'lv': 'Gdiņa', 'sk': 'Gdyňa', 'uk': 'Гдиня', 'pl': 'Gdynia', 'he': 'גדיניה', 'ja': 'グディニャ', 'eo': 'Gdinio'}, 'lat': 54.5164982, 'lon': 18.5402738, 'country': 'PL', 'state': 'Pomeranian Voivodeship'}
    actual_response1 = geolocate("gdynia")
    assert actual_response1 == expected_response1
    
    expected_response2 = {'name': 'San Francisco', 'local_names': {'it': 'San Francisco', 'hu': 'San Francisco', 'kn': 'ಸಾನ್ ಫ್ರಾನ್ಸಿಸ್ಕೊ', 'cs': 'San Francisco', 'ne': 'सान फ्रान्सिस्को', 'ro': 'San Francisco', 'pl': 'San Francisco', 'gv': 'San Francisco', 'mi': 'Hana Paraniko', 'ky': 'Сан-Франциско', 'ht': 'San Francisco', 'ga': 'San Francisco', 'pt': 'São Francisco', 'lv': 'Sanfrancisko', 'lt': 'San Fransiskas', 'ba': 'Сан-Франциско', 'eu': 'San Frantzisko', 'da': 'San Francisco', 'qu': 'San Francisco', 'bs': 'San Francisco', 'el': 'Σαν Φρανσίσκο', 'yo': 'San Francisco', 'la': 'Franciscopolis', 'fr': 'San Francisco', 'gd': 'San Francisco', 'co': 'San Francisco', 'tt': 'Сан-Франциско', 'ru': 'Сан-Франциско', 'zh': '旧金山;舊金山;三藩市', 'bn': 'সান ফ্রান্সিস্কো', 'ha': 'San Francisco', 'mk': 'Сан Франциско', 'fy': 'San Francisco', 'bo': 'སན་ཧྥུ་རན་སིས་ཁོ', 'kk': 'Сан-Франциско', 'uz': 'San Fransisko', 'mr': 'सॅन फ्रान्सिस्को', 'hi': 'सैन फ़्रांसिस्को', 'bg': 'Сан Франциско', 'sw': 'San Francisco', 'fi': 'San Francisco', 'vo': 'San Francisco', 'is': 'San Francisco', 'gl': 'San Francisco', 'io': 'San Francisco', 'ug': 'San Fransisko', 'sk': 'San Francisco', 'bm': 'San Francisco', 'fo': 'San Francisco', 'cv': 'Сан-Франциско', 'so': 'San Fransisko', 'no': 'San Francisco', 'ml': 'സാൻ ഫ്രാൻസിസ്കോ', 'af': 'San Francisco', 'sh': 'San Francisco', 'ms': 'San Francisco', 'sv': 'San Francisco', 'ko': '샌프란시스코', 'ar': 'سان فرانسيسكو', 'de': 'San Francisco', 'fj': 'San Francisco', 'ie': 'San Francisco', 'vi': 'Cựu Kim Sơn', 'kw': 'San Francisco', 'az': 'San-Fransisko', 'ps': 'سان فرانسسکو', 'ka': 'სან-ფრანცისკო', 'ur': 'سان فرانسسکو', 'hy': 'Սան Ֆրանցիսկո', 'uk': 'Сан-Франциско', 'mn': 'Сан-Франциско', 'sq': 'San Francisco', 'ln': 'San Francisco', 'tw': 'San Francisco', 'ca': 'San Francisco', 'nn': 'San Francisco', 'oc': 'San Francisco', 'na': 'San Francisco', 'id': 'San Francisco', 'an': 'San Francisco', 'br': 'San Francisco', 'te': 'శాన్ ఫ్రాన్సిస్కో', 'cy': 'San Francisco', 'am': 'ሳን ፍራንሲስኰ', 'nv': 'Naʼníʼá Hóneezí', 'ja': 'サンフランシスコ', 'my': 'ဆန်ဖရန်စစ္စကိုမြို့', 'tl': 'San Francisco', 'ta': 'சான் பிரான்சிஸ்கோ', 'ia': 'San Francisco', 'nl': 'San Francisco', 'lb': 'San Francisco', 'ku': 'San Francisco', 'ce': 'Сан-Франциско', 'pa': 'ਸਾਨ ਫ਼ਰਾਂਸਿਸਕੋ', 'yi': 'סאן פראנציסקא', 'he': 'סן פרנסיסקו', 'hr': 'San Francisco', 'mg': 'San Francisco', 'si': 'සැන් ෆ්\u200dරැන්සිස්කෝ', 'os': 'Сан-Франциско', 'sr': 'Сан Франциско', 'et': 'San Francisco', 'ki': 'San Francisco', 'li': 'San Francisco', 'sl': 'San Francisco', 'eo': 'San-Francisko', 'sc': 'San Francisco', 'jv': 'San Francisco', 'fa': 'سان فرانسیسکو', 'es': 'San Francisco', 'en': 'San Francisco', 'th': 'ซานฟรานซิสโก', 'tr': 'San Francisco', 'be': 'Сан-Францыска', 'ty': 'San Francisco'}, 'lat': 37.7790262, 'lon': -122.419906, 'country': 'US', 'state': 'California'}
    actual_response2 = geolocate("san francisco")
    assert actual_response2 == expected_response2

    assert geolocate("NotExistingLocation") == None
    # had to block rising error by the function so the bot will continue asking the user for an existing location
    #with pytest.raises(IndexError):
    #    geolocate("NotExistingLocation")


def test_get_weather_forecast():
    assert get_weather_forecast("Gdynia", "2023-04-10") == ({'location': 'Gdynia'}, {'temp_min': 3.4, 'temp_max': 8.7, 'temp_apparent_min': 3.4, 'temp_apparent_mmax': 3.4, 'sunrise': '05:54', 'sunset': '19:40', 'precipitation_probability': 6, 'precipitation_sum': 3.4, 'windspeed_max': 3.4}, {'temp': '°C', 'windspeed': 'km/h', 'precipitation': 'mm', 'probability': '%'})


def test_trim_weather_forcast_to_a_day(example_forecast_data):
    with pytest.raises(UnboundLocalError):
        # Check if proper error is raised if date is older than today or >7 days from today
        trim_weather_forcast_to_a_day("Gdynia", "2023-01-06", example_forecast_data)
    assert trim_weather_forcast_to_a_day("Gdynia", "2023-04-06", example_forecast_data) == ({'location': 'Gdynia'}, {'temp_min': 0.0, 'temp_max': 3.2, 'temp_apparent_min': 0.0, 'temp_apparent_mmax': 0.0, 'sunrise': '06:04', 'sunset': '19:32', 'precipitation_probability': 0, 'precipitation_sum': 0.0, 'windspeed_max': 0.0}, {'temp': '°C', 'windspeed': 'km/h', 'precipitation': 'mm', 'probability': '%'})