from datetime import date, datetime

import matplotlib.pyplot as plt
import numpy as np
import pytz

import requests

import covalent as ct

@ct.electron
def get_RA(target_list):
    RA = []
    for target_name in target_list:
        response = requests.get(
            "http://simbad.u-strasbg.fr/simbad/sim-id?output.format=votable&Ident=%s&output.params=ra,dec"
            % target_name
        )
        star_info = response.text
        RA.append(star_info[star_info.index("<TR><TD>") + 8 : star_info.index("</TD><TD>")])
    RA_degs = []
    for source in RA:
        hour = float(source.split(" ")[0])
        minute = float(source.split(" ")[1])
        second = float(source.split(" ")[2])
        RA_degs.append(((hour + minute / 60 + second / 3600) * 15))
    return RA_degs


@ct.electron
def get_dec(target_list):
    dec = []
    for target_name in target_list:
        response = requests.get(
            "http://simbad.u-strasbg.fr/simbad/sim-id?output.format=votable&Ident=%s&output.params=ra,dec"
            % target_name
        )
        star_info = response.text
        dec.append(star_info[star_info.index("</TD><TD>") + 9 : star_info.index("</TD></TR>")])
    dec_degs = []
    for source in dec:
        degree = float(source.split(" ")[0])
        arcmin = float(source.split(" ")[1])
        arcsec = float(source.split(" ")[2])
        if degree < 0:
            dec_degs.append(degree - arcmin / 60 - arcsec / 3600)
        else:
            dec_degs.append(degree + arcmin / 60 + arcsec / 3600)
    return dec_degs


@ct.electron
def days_since_J2000(region):
    f_date = date(2000, 1, 1)
    year = get_date(time_zone=region)[0]
    month = get_date(time_zone=region)[1]
    day = get_date(time_zone=region)[2]
    l_date = date(year, month, day)
    delta = l_date - f_date
    return delta.days


@ct.electron
def local_sidereal_time(d, long, T):
    LST = 100.46 + 0.985647 * (d + T / 24) + long + 15 * T
    return LST


@ct.electron
def hour_angle(LST, RA):
    LST_list = []
    for source in RA:
        LST_list.append(np.asarray([value - source for value in LST]))
    return LST_list


@ct.electron
def altitude_of_target(dec, lat, ha):
    alt_list = []
    lat = lat * 0.0174533
    for i in range(len(dec)):
        dec_i = dec[i] * 0.0174533
        ha_i = ha[i] * 0.0174533
        alt = np.arcsin(np.sin(dec_i) * np.sin(lat) + np.cos(dec_i) * np.cos(lat) * np.cos(ha_i))
        alt_list.append(alt * 57.2958)
    return alt_list


@ct.electron
def convert_to_utc(time_zone):
    start_time = 0
    end_time = 24.016
    now = datetime.now(pytz.timezone(time_zone))
    offset = now.utcoffset().total_seconds() / 60 / 60
    utc_timerange = np.arange(start_time - offset, end_time - offset, 0.016)
    return utc_timerange


@ct.electron
def get_date(time_zone):
    now = datetime.now(pytz.timezone(time_zone))
    year = now.year
    month = now.month
    day = now.day
    return [year, month, day]


@ct.electron
def get_azimuth(dec, lat, ha, alt):
    az_list = []
    lat = round(lat * 0.0174533, 2)
    for i in range(len(dec)):
        azimuth = []
        dec_i = round(dec[i] * 0.0174533, 2)
        ha_i = ha[i] * 0.0174533
        alt_i = alt[i] * 0.0174533
        a = np.arccos(
            (np.sin(dec_i) - np.sin(alt_i) * np.sin(lat)) / (np.cos(alt_i) * np.cos(lat))
        )
        for q in range(len(ha_i)):
            if np.sin(ha_i[q]) < 0:
                azimuth.append(a[q] * 57.2958)
            else:
                azimuth.append(360 - (a[q] * 57.2958))
        az_list.append(np.array(azimuth))
    return az_list
    
    
    
@ct.lattice
def final_calc(
    target_list=["sirius", "trappist-1"],
    region="America/Los_Angeles",
    latitude=49.2827,
    longitude=-123.1207,
):
    RA = get_RA(target_list=target_list)
    dec = get_dec(target_list=target_list)
    T = convert_to_utc(time_zone=region)
    d = days_since_J2000(region=region)
    lst = local_sidereal_time(d=d, long=longitude, T=T)
    ha = hour_angle(LST=lst, RA=RA)
    alt = altitude_of_target(dec=dec, lat=latitude, ha=ha)
    az = get_azimuth(dec=dec, lat=latitude, ha=ha, alt=alt)
    return alt, az

final_calc.draw(target_list=["sirius", "trappist-1"], region="America/Los_Angeles", latitude=49.2827, longitude=-123.1207)
altitude_azimuth = ct.dispatch_sync(final_calc)()
print(altitude_azimuth.result)
