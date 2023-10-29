# UK and Ireland tide time model (with predictions)

Tide clocks assume that high tide is spaced every 12 hours and 25 minutes.  They look good, but on average they have about 38 minutes of error (one standard deviation), however a little modelling can get this down to 9 minutes of error.  The deviation from uniform spacing is modelled as a sum of sinusoids and parameters fitted with least-mean-squared error.

Python/micropython code is provided to read the model and compute predictions.   This work is part of the TideClock app in [wasp-os](https://github.com/wasp-os/wasp-os)

Here are predictions for [2024](https://drtonyr.github.io/tide/2024/) - if you need more accuracy go to the [BBC](https://www.bbc.co.uk/weather/coast-and-sea/tide-tables).
