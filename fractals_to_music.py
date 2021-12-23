import mathematics_of_music
import numpy as np
from enum import Enum
from lsystem import Lsystem
from scipy.io.wavfile import write


class Note:
    """
    Class used to keep track of the pitch and duration of a given note
    """

    def __init__(self, pitch, duration):
        """
        Parameters
        ----------
        pitch : int
            Integer value representing the pitch of the note
        duration : int
            Integer value representing the duration of the note
        """
        # Uses mod 7 to allow for an infinite range of pitches
        # This does unfortunately mean though that the outputted music will be less accurate.
        self.pitch = pitch % 7
        self.duration = duration
        self.pitch_map = {
            0: 'C',
            1: 'D',
            2: 'E',
            3: 'F',
            4: 'G',
            5: 'A',
            6: 'B'
        }

    def __str__(self):
        note_char = self.pitch_map[self.pitch]
        return '{}-'.format(note_char) * self.duration


class Dir(Enum):
    """
    Enum used to keep track of the turtle direction when converting the L-system to music
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def turn_right(d):
    """
    Method used to turn the turtle to the right

    Parameters
    ----------
    d : Dir
        Direction meant to be turned to the right

    Returns
    -------
    Dir
        Dir resulting from the turn
    """
    return_val = None
    if d == Dir.UP:
        return_val = Dir.RIGHT
    elif d == Dir.RIGHT:
        return_val = Dir.DOWN
    elif d == Dir.DOWN:
        return_val = Dir.LEFT
    elif d == Dir.LEFT:
        return_val = Dir.UP
    return return_val


def turn_left(d):
    """
    Method used to turn the turtle to the left

    Parameters
    ----------
    d : Dir
        Direction meant to be turned to the left

    Returns
    -------
    Dir
        Dir resulting from the turn
    """
    return_val = None
    if d == Dir.UP:
        return_val = Dir.LEFT
    elif d == Dir.RIGHT:
        return_val = Dir.UP
    elif d == Dir.DOWN:
        return_val = Dir.RIGHT
    elif d == Dir.LEFT:
        return_val = Dir.DOWN
    return return_val


if __name__ == '__main__':

    # Gathers user input
    fractal_file = input('Enter the location of the L-system file: ')
    iterations = input('How many times should the L-system be iterated? [3] ')
    if iterations.isnumeric():
        iterations = int(iterations)
    else:
        iterations = 3  # Default value
    starting_direction = input('What should the turtle starting direction be when interpreting L-system music? '
                               '(Enter up, down, left, or right) [up]')
    if starting_direction.lower() == 'left':
        starting_dir = Dir.LEFT
    elif starting_direction.lower() == 'down':
        starting_dir = Dir.DOWN
    elif starting_direction.lower() == 'right':
        starting_dir = Dir.RIGHT
    else:
        starting_dir = Dir.UP  # Default value
    draw_image = input('Do you want the L-system to be drawn? (Enter Y/N) [N] ').lower() in ['y', 'yes', 'true', 't']

    print()  # Print statement to separate input from output

    lsystem = Lsystem(draw_image=draw_image)
    lsystem.compile('{}'.format(fractal_file), iterations)
    if draw_image:
        lsystem.draw()

    notes = []
    current_pitch = 0
    current_duration = 0
    direction = starting_dir
    generated_str = lsystem.generation[-1]

    movement_chars = {'F', 'A', 'B'}
    for character in generated_str:
        if character in movement_chars:

            # Records the duration and pitch of the tones based on the turtle movements
            if direction == Dir.LEFT or direction == Dir.RIGHT:
                current_duration += 1
            elif direction == Dir.UP:
                current_pitch += 1
                current_duration = 0
            elif direction == Dir.DOWN:
                current_pitch -= 1
                current_duration = 0

        elif character == '+' or character == '-':
            if (direction == Dir.LEFT or direction == Dir.RIGHT) and current_duration:
                # Pops out the previous tone if the pitches match.
                # This is to keep the current pitch duration accurate.
                if notes and notes[-1].pitch == current_pitch and \
                        (notes[-1].duration == current_duration - 1 or
                         notes[-1].duration == current_duration):
                    notes.pop()
                notes.append(Note(current_pitch, current_duration))

            if character == '+':
                direction = turn_right(direction)
            elif character == '-':
                direction = turn_left(direction)

    music_str = ''
    for note in notes:
        music_str += str(note)

    print('Saving the music files...')

    samplerate = 44100

    try:
        data = mathematics_of_music.get_song_data(music_str, duration=0.5)
        data = data * (16300 / np.max(data))
        write('audio_files/{}.wav'.format(lsystem.name), samplerate, data.astype(np.int16))

        reverse_music_notes = ''
        for val in range(len(notes) - 1, -1, -1):
            reverse_music_notes += str(notes[val])
        data = mathematics_of_music.get_song_data(reverse_music_notes, duration=0.5)
        data = data * (16300 / np.max(data))
        write('audio_files/{}_reverse.wav'.format(lsystem.name), samplerate, data.astype(np.int16))
    except FileNotFoundError as err:
        print(err)
    else:
        print('Successfully wrote the music files for {}'.format(lsystem.name))

    if draw_image:
        print()
        input('Please press enter when finished.\n')  # Used to keep the image open
