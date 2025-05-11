# HOMM3 Army Power Dashboard

> In the beginning, there was only chaos and the README, an eldritch slab of markdown, squatting at the root of every repo, staring back at you with the blank, expectant gaze of a peasant conscript about to meet a Black Dragon. Welcome, traveler, to the Army Power Dashboard, a Streamlit app where the mundane arithmetic of war is elevated to a cosmic ballet of numbers, spreadsheets, and existential dread.

---

## Table of Contents

- [What Is This?](#what-is-this)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Epilogue](#epilogue)

---

## What Is This?

Behold: a dashboard that splits the world in twain-on the left, your own battered legions; on the right, the enemy, their faces as familiar and yet as unknowable as your own reflection in a puddle after a rainstorm that smells faintly of sulfur and regret.

Each army is a procession of seven empty slots, yearning to be filled. Here, you will inscribe the names of units: Pikeman, Angel, Peasant: names that echo through the halls of memory like the footsteps of a tax collector in an abandoned village. You will enter their numbers, as if counting the grains of sand in an hourglass that measures not time, but the slow erosion of hope.

And then, the Power Score:  
$$
\text{Power Score} = (\text{Attack} + \text{Defence} + \text{Speed} + \frac{\text{Min Damage} + \text{Max Damage}}{2}) \times \text{Health}
$$
A formula so simple, so profound, it mocks the futility of all human endeavor.

---

## Features

- **Dual Army Display:** Two columns-like the twin pillars of Solomon’s temple, or the legs of a table that wobbles on the uneven floor of fate.
- **Seven Slots per Army:** Because six is too few and eight is hubris.
- **Unit Input:** Name your units, count your units, realize too late that you have chosen poorly.
- **Real-Time Power Calculation:** Watch as your hopes are quantified and found wanting.
- **Unit Stat Display:** Each stat a tiny window into the soul of a creature doomed to die for your glory.
- **Army Totals:** At the bottom, the sum of all fears: total power and maximum speed, staring up at you like the eyes of a hungry dog.
- **Error Handling:** Enter a unit name incorrectly and the app will rebuke you, gently, like a disappointed parent.

---

## Installation

1. **Clone this repository**  
   `git clone https://github.com/alibekk93/HOMM3_army_dashboard.git`

2. **Install dependencies**  
   `pip install streamlit pandas`

3. **Check the sacred CSV**  
   Make sure that `H3Units_Enhanced.csv` in the project directory in `data` folder.  
   (This file is the Book of Names-without it, the dashboard is a hollow shell, a golem without a soul.)

---

## Usage

1. **Run the app**  
   `streamlit run army_calculator.py`

2. **Behold the dashboard**  
   A page will open. Two armies glare at each other across the digital void.  
   Enter unit names and numbers.  
   Watch as the Power Score blooms and withers before your eyes.

3. **Interpret the results**  
   Are you stronger? Faster? Or merely more numerous, like locusts before the harvest?

---

## Screenshots

*Here, a screenshot would appear, but in its absence, imagine a battlefield at dusk:  
Columns of numbers marching to their doom, led by a single, blinking cursor.*

---

## Contributing

To contribute is to embrace futility, and yet, what is life but a series of futile gestures performed with increasing desperation? Fork, branch, submit a pull request.  
Correct a typo, add a feature, or simply scream into the void.  
All are welcome. None will be remembered.

---

## License

MIT.  
A license as permissive as the wind, as indifferent as the grave.

---

## Epilogue

In the end, the dashboard is but a mirror. You gaze into it, searching for power, for victory, for meaning.  
It gazes back, silent and implacable, and you realize:  
The true enemy was the README all along.