from yta_validation.parameter import ParameterValidator
from yta_validation import PythonValidator
from yta_programming.decorators.requires_dependency import requires_dependency
from typing import Union

import numpy as np
import librosa


class Audio:
    """
    Class to represent an audio and to be able
    to handle it work with it easy.
    """

    @property
    def number_of_channels(
        self
    ) -> int:
        """
        The number of channels of the audio.
        """
        shape = self.audio.shape

        return (
            1
            if len(shape) == 1 else
            shape[1]
        )

    @property
    def number_of_samples(
        self
    ) -> int:
        """
        The number of samples in the audio.
        """
        return self.audio.shape[0]

    @property
    def is_mono(
        self
    ) -> bool:
        """
        Check if the audio is mono (includes
        only one channel) or not.
        """
        return self.number_of_channels == 1
    
    @property
    def is_stereo(
        self
    ) -> bool:
        """
        Check if the audio is stereo (includes
        two channels) or not.
        """
        return self.number_of_channels == 2
    
    # Other properties below
    @property
    def min(
        self
    ):
        """
        Get the min value of the audio.
        """
        return np.min(np.abs(self.audio))

    @property
    def max(
        self
    ):
        """
        Get the max value of the audio.
        """
        return np.max(np.abs(self.audio))
    
    @property
    def inverted(
        self
    ) -> np.ndarray:
        """
        Get the audio but inverted as an horizontal mirror.

        TODO: Wtf is this (?)
        """
        return -self.audio
    
    @property
    def reversed(
        self
    ) -> np.ndarray:
        """
        Get the audio but reversed.
        """
        return self.audio[::-1]
    
    @property
    def normalized(
        self
    ) -> np.ndarray:
        """
        Get the audio but normalized, which means that its
        maximum value is 1.0.
        """
        max_val = np.max(np.abs(self.data))
        if max_val > 0:
            self.data /= max_val

    def __init__(
        self,
        audio: Union['np.ndarray', str],
        sample_rate: Union[int, None] = None
    ):
        # 1. Process a filename
        if PythonValidator.is_string(audio):
            # TODO: Use 'try-catch' or validate audio file
            # sr=None preserves the original sample rate
            audio, sample_rate = librosa.load(audio, sr = sample_rate)
            self.sample_rate = sample_rate

        # TODO: Process 'AudioClip', etc...
        # 2. Process a numpy array
        # TODO: Handle the type and process the input
        # TODO: Set the accepted input types
        # TODO: What about the sample rate (?)
        self.audio: Union['np.ndarray'] = audio
        """
        The audio numpy array once that has been read
        according to the input.
        """
        self.sample_rate = sample_rate
        """
        The sample rate of the audio. If you force this
        value pay attention because the result could be
        unexpected if it is not an accurate value.
        """

        if (
            not self.is_mono and
            not self.is_stereo
        ):
            raise Exception('The format is unexpected, no mono nor stereo audio.')
        
    # TODO: This is for an audio frame, not necessary for
    # the whole audio, but an audio is also an audio
    # frame
    def change_audio_volume(
        self,
        audio_frame: np.ndarray,
        factor: int = 100
    ):
        """
        Change the 'audio_frame' volume by applying the
        given 'factor'.

        Based on:
        https://github.com/Zulko/moviepy/blob/master/moviepy/audio/fx/MultiplyVolume.py
        """
        # TODO: Apply the limit better
        ParameterValidator.validate_mandatory_int('factor', factor)

        factors_array = np.full(self.number_of_samples, factor)

        return (
            np.multiply(
                audio_frame,
                factors_array
            )
            if self.is_mono else
            np.multiply(
                audio_frame,
                factors_array[:, np.newaxis]
            )
            # if self.is_stereo == 2:
        )
    
    @requires_dependency('soundfile', 'yta_audio_editor', 'soundfile')
    def save(
        self,
        filename: str
    ):
        """
        Write the audio to a file with the given
        'filename'.
        """
        import soundfile as sf

        sf.write(filename, self.data, self.sample_rate)

    # TODO: This 'sounddevice' library is not very stable
    # nor working always... and playing the sound is not
    # an important need now...
    # @requires_dependency('sounddevice', 'yta_audio_editor', 'sounddevice')
    # def play(
    #     self
    # ):
    #     """
    #     Play the audio until it finishes.
    #     """
    #     import sounddevice as sd

    #     sd.play(self.data, self.sample_rate)
    #     sd.wait()

    # TODO: These methods are modifying the numpy and
    # returning a new array modified, but not modifying
    # the original audio instance
    def with_fadein(
        self,
        duration: float
    ):
        """
        Get the audio with a fade in effect applied. This
        method does not modify the original audio but
        returns the audio modified.
        """
        number_of_samples = int(duration * self.sample_rate)
        fade = np.linspace(0, 1, number_of_samples)

        return self.audio[:number_of_samples] * fade[:, np.newaxis]
    
    def with_fadeout(
        self,
        duration: float
    ):
        """
        Get the audio with a fade out effect applied. This
        method does not modify the original audio but 
        returns the audio modified.
        """
        number_of_samples = int(duration * self.sample_rate)
        fade = np.linspace(1, 0, number_of_samples)

        return self.audio[-number_of_samples:] * fade[:, np.newaxis]
    
    def time_stretch(
        self,
        rate
    ):
        """
        TODO: Explain what is 'time stretching' and what
        is the 'rate' parameter.
        """
        y = librosa.to_mono(self.audio.T)
        y_stretched = librosa.effects.time_stretch(y, rate)

        audio = y_stretched[:, np.newaxis]
        number_of_samples = audio.shape[0]

        # TODO: Not nice return...
        return audio, number_of_samples

    def pitch_shift(
        self, 
        n_steps
    ):
        """
        TODO: Explain what is 'pitch shifting' and what
        is the 'n_steps' parameter.
        """
        y = librosa.to_mono(self.audio.T)
        y_shifted = librosa.effects.pitch_shift(y, self.sample_rate, n_steps)

        audio = y_shifted[:, np.newaxis]
        number_of_samples = audio.shape[0]

        # TODO: Not nice return...
        return audio, number_of_samples
    
    @requires_dependency('scipy', 'yta_audio_editor', 'scipy')
    def apply_filter(
        self,
        cutoff,
        btype = 'low',
        order = 5
    ):
        """
        Apply a filter.

        TODO: Explain this better, I don't know what is
        this method doing.
        """
        from scipy.signal import butter, lfilter

        nyq = 0.5 * self.sample_rate
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype=btype)
        # We need a copy to preserve the original
        audio = self.audio.copy()
        for ch in range(self.number_of_channels):
            audio[:, ch] = lfilter(b, a, self.data[:, ch])

        return audio

    def fft(self):
        """
        Get the magnitude of the Fourier spectrum per
        channel.
        """
        return np.abs(np.fft.rfft(self.audio, axis = 0))