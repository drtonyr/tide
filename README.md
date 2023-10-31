# UK and Ireland tide time model (with predictions)

Tide clocks assume that high tide is spaced every 12 hours and 25 minutes.  They look good, but on average they have about 38 minutes of error (one standard deviation), however a little modelling can get this down to 9 minutes of error.  The deviation from uniform spacing is modelled as a sum of sinusoids and parameters fitted with least-mean-squared error.

This is good enough for holiday use, whether it's planning which week to go on holiday or to avoid being cut off by high tides.  If you need more accuracy go to the [BBC](https://www.bbc.co.uk/weather/coast-and-sea/tide-tables) or buy.

Python/micropython code is provided to read the model and compute predictions for any year.  This work is part of the TideClock app in [wasp-os](https://github.com/wasp-os/wasp-os)

Predictions are provided for [2024](2024) and [2025](2025).  Ask me if you need later predictions and you can't run the code.
