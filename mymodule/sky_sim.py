#! /usr/bin/python3 python
"""Determine Andromeda location in ra/dec degrees"""

from math import cos,pi
from random import uniform
import argparse
import logging

# configure logging (in global scope)
logging.basicConfig(format="%(asctime)s, %(name)s:%(levelname)s %(message)s", level=logging.DEBUG)
log = logging.getLogger("mylogger") # get or create a logger


NSRC = 1_000_000
# from wikipedia
RA_STR = '00:42:44.4'
DEC_STR = '41:16:08'

def get_radec():
    """
    Generate the ra/dec coordinates of Andromeda
    in decimal degrees.

    Returns
    -------
    ra : float
        The RA, in degrees, for Andromeda
    dec : float
        The DEC, in degrees for Andromeda
    """
    log.debug('Entering get_radec')

    # from wikipedia
    andromeda_ra = '00:42:44.3'
    andromeda_dec = '41:16:09'

    d, m, s = andromeda_dec.split(':')
    dec = int(d)+int(m)/60+float(s)/3600

    h, m, s = andromeda_ra.split(':')
    ra = 15*(int(h)+int(m)/60+float(s)/3600)
    ra = ra/cos(dec*pi/180)
    log.debug('Exiting get_radec') 
    return ra,dec


def make_positions(ra, dec, nsrc=NSRC):
    """
    Generate NSRC stars within 1 degree of the given ra/dec

    Parameters
    ----------
    ra,dec : float
        The ra and dec in degrees for the central location.
    nsrc : int
        The number of star locations to generate
        Default = mymodule.sky_sim.NSRC
    
    Returns
    -------
    ras, decs : list
        A list of ra and dec coordinates.
    """
    log.debug('Entering make_positions')

    # make 1000 stars within 1 degree of Andromeda
    ras = []
    decs = []
    for i in range(nsrc):
        ras.append(ra + uniform(-1,1))
        decs.append(dec + uniform(-1,1))
    # apply a filter
    ras,decs = crop_to_circle(ras,decs,ra,dec,1)
    log.debug(f'Exiting make_positions with {ra}, {dec}, {nsrc}') 
    return ras,decs

def crop_to_circle(ras, decs, ref_ra, ref_dec, radius):
    """
    Crop an input list of positions so that they lie within radius of
    a reference position

    Parameters
    ----------
    ras,decs : list(float)
        The ra and dec in degrees of the data points
    ref_ra, ref_dec: float
        The reference location
    radius: float
        The radius in degrees
    Returns
    -------
    ras, decs : list
        A list of ra and dec coordinates that pass our filter.
    """
    log.debug('Entering crop_to_circle')

    ra_out = []
    dec_out = []
    for i in range(len(ras)):
        if (ras[i]-ref_ra)**2 + (decs[i]-ref_dec)**2 < radius**2:
            ra_out.append(ras[i])
            dec_out.append(ras[i])
    log.debug('Exiting crop_to_circle') 
    return ra_out, dec_out

def save_positions(ras, decs, out='catalog.csv'):

    # now write these to a csv file for use by my other program
    with open(out,'w',encoding='utf8') as f:
        print("id,ra,dec",file=f)
        for i in range(len(ras)):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}",file=f)
    log.info(f'Writing file {out}') 


def skysim_parser():
    """
    Configure the argparse for skysim

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser for skysim.
    """

    parser = argparse.ArgumentParser(prog='sky_sim', prefix_chars='-')
    parser.add_argument('--ra', dest = 'ra', type=float, default=None,
                        help="Central ra (degrees) for the simulation location")
    parser.add_argument('--dec', dest = 'dec', type=float, default=None,
                        help="Central dec (degrees) for the simulation location")
    parser.add_argument('--out', dest='out', type=str, default='catalog.csv',
                        help='destination for the output catalog')
    return parser


def main():
    parser = skysim_parser()
    options = parser.parse_args()
    # if ra/dec are not supplied the use a default value
    if None in [options.ra, options.dec]:
        ra, dec = get_radec()
    else:
        ra = options.ra
        dec = options.dec

    ras, decs = make_positions(ra, dec, NSRC)
    save_positions(ras, decs, options.out)


if __name__ == "__main__":
    main()
