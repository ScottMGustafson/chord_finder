# Chord Finder

Python Script to generate all possible chords from specified scale. Possible chord definitions and 
scale definitions are specified in `chord_config.yml`.  I essentially use this as a compositional tool
to find chords that fit with a particular mode I'm playing with.  Nothing more.

Run the script in the shell like:

```
$ python chord_finder.py <pitch> <mode_name>
```
_e.g._ for the whole tone scale:
```
$ python chord_finder.py G messiaen_mode_1
 - G +
 - A +
 - B +
 - C#+
 - D#+
 - F +
```
or import into your python environment.

I've provided a conda environment to use, but considering the minimal number of packages this script imports from, 
you likely will not need it.

## Specifying Additional Chords
In the `chord_config.yml`, chords are specified as the chromatic separation between the root and each pitch of that 
chord as a tuple. For instance, a diatonic major chord will be:
```yaml
chord_definitions:
  M: (4, 7)
```
since the major third is 4 semitones and the perfect fifth is 7 semitones above the root, respectively.

## Specifying additional scales
here, each field is a list of intervalic separations between adjacent tones (in units of semitones.) so that
```yaml
mode_definitions:
  # whole tone scale, aka messiaen mode 1
  whole_tone: [2, 2, 2, 2, 2]
```
