# ClimateSensitivity

Using surface station data to measure climate sensitivity.

We will stipulate as uncontroversial facts that increased carbon dioxide in the atmosphere has a warming effect on the earths surface.  That effect is  proportional to the logarithm of any concentraion change over any period such that a doubling of CO2 adds 3.7 watts per meter squared of radiation downward to the earths surface.  The resulting formula is

Power = 5.35 ln(c/C0) in watts per meter squared

An interesting and more controversial question is what temperature rise may be expected from this increased radiant heat load.  This repo implements a simple method to measure climate  sensitivty directly across datasets that contain radiant heat and average surface temperatures at selected sites across both northern and southern hemisphere. The resulting sensitvities range from 0.16 to 0.22 degrees K per watt per meter squared.  In contrast, IPCC calims  that sensitivty is 0.8 +/- 0.4 K per watt per meeter squared. Here is an example plot of the data:

![climate sens](figure_1.png)

Our fiure 1 graph, shows GISS attionstation temperature vs. cloud refelction corrected inout power. Temperature, lattitude, longtiude, and elevation data comes [from NASA](https://data.giss.nasa.gov/gistemp/stdata/).  The top of atmosphere (TOA) solar input power is calculated from the tables provided [here](http://applet-magic.com/insolation.htm).  The python program clisen.py

1. Corrects TOA power for cloud reflections and lattitude
2. Applies albedo correction to those powers
3. calculates separate sensitivities for northern and southern hemisphere using both cloud/lattitude corrected solar power and powerthat power corrected for albedo.

The raw power produces slightly higher sensitivities as the albedo correction has the effect of increasing input power differences from polar area to equator.  The following table shows the caluclated sensitivies for raw and corrected power. The graph illustrates the response we actually see on earth, about 38 degrees C for 200 watts flux increase. In comparison IPCC low-end and best estimates of climate sensiticity rise 40 or 80 degrees for 100 watts flux increase.

  Hemispere|cloud/latt corrected|+ albedo corrected|
 --|------|-----|
 N|0.179|0.159|
 S|0.219|0.191|

One great advantage of this method is that there is plenty of signal here.  Temperature ranges across 60 degrees K and power ranges over 250 watts per meter squared. Disputes over small adjustments in temperature, common when looking at time series temperature data to tease out the magnitude of CO2 driven warming,  will not have much effect on these measured sensitivities.  Revviewers or critics might come foreward with some valid criticisms of how power numbers are calculated.  For example one can argue we need a different, better albedo correction or we need to incorporate downward IR power into radiant heat numbers.  But again neither of those will change the range of the results significantly. Adding in downward IR is likely to reduce sensitivity since inevitably there is more IR heating in the hot, wet tropics than the cold, dry poles.  The albedo correction I use is based on lattitude from this [table](http://www.climatedata.info/forcing/albedo/).  I would like to replace it with something that uses, say ISCCP satellite data or the mix of land types and land to sea ratios in the region of influence around a given station.


What can account for the differences between sensitivities obtained here and the IPCC numbers, which are famously derived from models with significant, amplifying feedbacks on CO2 driven warming?  It is uncontroversial that the climate systems has potential feedbacks that are positive, i.e. amplify CO2 driven warming, and also potential negative atennuating feedbacks that counteract CO2 driven warming.  Another great advantage of this method is that all feedbacks are necessarily integrated and superposed into the measured data. Arguments that CO2 IR warming carries some special amplifying inducing properties that raw solar does not will be a hard sell to people with solid understandings of basic physics.    

The station data is summarized in csv files for each hemishpere. Clisen.py uses [pandas](https://pandas.pydata.org) to read in the files.  pdfs of each station historical record of temperature are archived in the tempdata folder.

I should note that stations were selected to cover as wide a range of the globe as possible with a strong bias towards stations at or near sea level, given the constraints of NASA GISS data coverage. The most outstanding exceptionTo this criteria is the Anmundsen Scott station at the South Pole at an elevation of 2835 meters.  This station's temperature wasis corrected back to sea level using lapse rate of ~2C per 300 meters.  Next highest elevation station is Banglaore at 920 meters. Its GISS temperature is not correctecd.


This whole exercise was Inspired by this [blog post](https://wattsupwiththat.com/2017/01/05/physical-constraints-on-the-climate-sensitivity/) on climate sensitivty which demonstrates a strong fit between a simple gray body model of eath's atomosphere and satellite ISCCP data on clouds and radiation in and out of atmosphere.

An important insight is that climate sensitivity, a function of power that returns seasonally averaged temperature at any location, is a continuous function across the globe and through time. It is also, for all practical purposes, (coninuously differentiable](https://en.wikipedia.org/wiki/Smoothness) and perhaps [analytic](https://en.wikipedia.org/wiki/Analytic_function).  The ratio of temperature to power from the poles to the equator is a ground truth refutation of  IPCC alarmist seesitivities.
