from pyraf import iraf
from pyraf.iraf import gemini
from pyraf.iraf import gemtools
from pyraf.iraf import gnirs

from pyGnirsIFU.reduction import parameters
from pyGnirsIFU.reduction import reduction

iraf.unlearn(gemini)
iraf.unlearn(gemtools)
iraf.unlearn(gnirs)



