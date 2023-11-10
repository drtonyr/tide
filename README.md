# Tide time model (with predictions)

Tide clocks assume that high tide is spaced every 12 hours and 25 minutes.  They look good, but on average they have about 38 minutes of error (one standard deviation), however a little modelling can get this down to 9 minutes of error.  The deviation from uniform spacing is modelled as a sum of sinusoids and parameters fitted with least-mean-squared error (for details see [Tidal Analysis and Prediction](https://tidesandcurrents.noaa.gov/publications/Tidal_Analysis_and_Predictions.pdf)).  This is good enough for holiday use, whether it's planning which week to go on holiday or to avoid being cut off by high tides.  If you need more accuracy then go online or buy.

Python/micropython code is provided to read the model and compute predictions for any time or a complete year.  Many sites in the UK and Ireland are modeled explicitly, for other locations there exists sites named `custom 0h00m` to `custom 12h20m`, just pick the site that matches the current tide.  Predictions are provided for [2024](2024) and [2025](2025).  Ask me if you need later predictions and you can't run the code.

This work is part of the TideClock app in [wasp-os](https://github.com/wasp-os/wasp-os).
