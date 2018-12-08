"""
generate all possible chords from specified scale.

Possible chord definitions and scale definitions are specified in `config.yml`

run as a shell script like:

```
$ python chord_finder.py G messiaen_mode_5
```
or import into your python environment.
"""

import doctest
import sys

import yaml


def generate_pitch_names(starting_pitch='C', sharped=True):
    """
    generate pitch name-integer index dict.

    Parameters
    ----------
    starting_pitch : str
        note name must be capitalized with `#` or `b` corresponding to sharp or flat respectively
    sharped : bool (default True)
        if True, use sharps rather than flats for the chromatic, otherwise use the enharmonic equivalents

    Returns
    -------
    dict
        dict of pitch names and corresponding integers
        examples:
            {'C': 0, 'C#': 1, ...}

    Examples
    --------
    >>> dct = generate_pitch_names(starting_pitch='C')
    >>> dct[0]
    'C'
    >>> generate_pitch_names(starting_pitch='D', sharped=False)[1]
    'Eb'
    >>> generate_pitch_names(starting_pitch='D', sharped=True)[1]
    'D#'
    """
    if 'b' in starting_pitch and sharped:
        sharped = False
    if sharped:
        pitch_names = 'C C# D D# E F F# G G# A A# B'.split(' ')
    else:
        pitch_names = 'C Db D Eb E F Gb G Ab A Bb B'.split(' ')

    pitches = {k: i for i, k in enumerate(pitch_names)}
    diff = pitches[starting_pitch] - pitches['C']
    return {reset_octave(i - diff): k for i, k in enumerate(pitch_names)}


def reset_octave(num):
    """
    Reset number outside of octave back into octave.

    Parameters
    ----------
    num : int
        number to reset

    Returns
    -------
    int

    Examples
    --------
    >>> reset_octave(13)
    1
    >>> reset_octave(0)
    0
    >>> reset_octave(-1)
    11
    """
    while num < 0:
        num += 12
        if num > 11:
            raise Exception('Not Possible: {}'.format(num))
    while num > 11:
        num -= 12
        if num < 0:
            raise Exception('Not Possible: {}'.format(num))
    return num


def name_chord(root, interval_tup, pitch_dct, chord_intervals):
    """
    returns a name of a chord

    Parameters
    ----------
    root : int
        root pitch as integer in pitch dict
    interval_tup : tuple
        interval separations from root as ints
    pitch_dct : dict
        pitch dictionary
    chord_intervals : dict
        interval:chord name key:value pairs

    Returns
    -------
    str
        chord name

    Examples
    --------
    >>> dct = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
    ...        6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
    >>> interval_dct = {(3, 7): 'm', (3, 7, 10): 'm7', (3, 6, 10): 'm7b5'}
    >>> name_chord(0, (3, 7), dct, interval_dct)
    'C m'
    >>> name_chord(2, (3, 7, 10), dct, interval_dct)
    'D m7'
    """
    return "{0: <2}{1:}".format(pitch_dct[root], chord_intervals[interval_tup])


def pretty_print_dict(chord_dct):
    """
    print a chord dictionary

    Parameters
    ----------
    chord_dct : dict
        keys are pitch names, values are lists of strings

    Returns
    -------
    None

    """
    for k, v in chord_dct.items():
        for x in sorted(v):
            print(' - {}'.format(x))
        #print('\n')


def get_possible_chords(mode, pitch_dct, chord_intervals):
    """
    function to find all possible chords within a given mode

    Parameters
    ----------
    mode : list
    pitch_dct : dict
    chord_intervals : dict

    Returns
    -------
    dict
        dict of possible chords where keys are pitch names (str) and values are lists of strings
    """
    dct = {}
    for root in mode:
        root = reset_octave(root)
        possible_chords = []
        for it in chord_intervals.keys():
            if all([reset_octave(root + x) in mode for x in it]):
                possible_chords.append(name_chord(root, it, pitch_dct, chord_intervals))
        if possible_chords:
            dct[root] = possible_chords
    return dct


def convert_seps(lst):
    """
    convert list of pitch separations to list of degrees on chromatic scale.  There will always
    be n+1 elements for a list of length n
    
    Parameters
    ----------
    lst : list
        list of integer pitch separations

    Returns
    -------
    list

    Examples
    --------
    >>> convert_seps([1,1,1,1])
    [0, 1, 2, 3, 4]
    """
    return [0, ] + [sum(lst[0:i+1]) for i in range(len(list(lst)))]


def proc_config_info(cfg_file):
    """
    parse config file

    Parameters
    ----------
    cfg_file : str
        path to config file

    Returns
    -------
    dict
        config info parsed from yaml file
    """
    cfg = yaml.load(open(cfg_file, 'r'))
    # interval seps of pitches in chords
    intervals = {tuple(eval(v)): k for k, v in cfg['chord_definitions'].items()}
    # convert interval seps to chromatic scale degrees
    # print(cfg['mode_definitions'])
    # raise Exception()
    modes = {k: convert_seps(v) for k, v in cfg['mode_definitions'].items()}
    return modes, intervals


def chord_finder(*args):
    """
    print all possible chords to stdout

    Parameters
    ----------
    args : tuple
        (<reference pitch name: str>, <mode name: str>)

    Returns
    -------
    None
    """
    pitch, mode = args[0], args[1]
    modes, intervals = proc_config_info('chord_config.yml')

    pitch_names = generate_pitch_names(starting_pitch=pitch)
    mode_lst = modes[mode]
    pretty_print_dict(get_possible_chords(mode_lst, pitch_names, intervals))


if __name__ == '__main__':
    doctest.testmod()
    chord_finder(*sys.argv[1:])
