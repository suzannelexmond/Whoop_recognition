#!/usr/bin/env python3
import os
import argparse
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample

try:
    from pycbc.types import TimeSeries
    from pycbc.filter import matchedfilter
except ImportError:
    os.system("pip install pycbc")
    from pycbc.types import TimeSeries
    from pycbc.filter import matchedfilter


def align_sampling(ts_a, ts_b):
    """Resample ts_b to match delta_t and length of ts_a."""
    if ts_a.delta_t == ts_b.delta_t and len(ts_a) == len(ts_b):
        return ts_a, ts_b

    N = len(ts_a)
    data_resampled = resample(ts_b.numpy(), N)
    ts_b_new = TimeSeries(data_resampled, delta_t=ts_a.delta_t)
    return ts_a, ts_b_new


def pad_or_truncate(ts_mimic, ts_match):
    """Adjust ts_mimic to have the same length as ts_match."""
    ts_match, ts_mimic = align_sampling(ts_match, ts_mimic)
    data_mimic = ts_mimic.numpy()
    if len(data_mimic) < len(ts_match):
        pad_width = len(ts_match) - len(data_mimic)
        data_mimic = np.pad(data_mimic, (0, pad_width), mode="constant")
    else:
        data_mimic = data_mimic[:len(ts_match)]
    return ts_match, TimeSeries(data_mimic, delta_t=ts_mimic.delta_t)


def compare_mimic(wav_file_mimic, wav_file_real, low_frequency_cutoff=10, high_frequency_cutoff=600):
    # If recording is too noisy, return score=0.0 to prevent match function error
    try:
        rate_mimic, data_mimic = wavfile.read(wav_file_mimic)
        rate_real, data_real = wavfile.read(wav_file_real)

        dataM1 = data_mimic.astype(np.float32)
        dataR1 = data_real.astype(np.float32)

        ts1 = TimeSeries(dataM1, delta_t=1.0/rate_mimic, dtype=np.float64)
        ts_real = TimeSeries(dataR1, delta_t=1.0/rate_real, dtype=np.float64)

        ts_real, ts1 = pad_or_truncate(ts1, ts_real)

        m1, idx = matchedfilter.match(
            ts1, ts_real,
            psd=None,
            low_frequency_cutoff=low_frequency_cutoff,
            high_frequency_cutoff=high_frequency_cutoff
        )

        mean_match = m1 / 0.5
        if mean_match > 1.0:
            mean_match = 1.0

        # print('Mean match of mimic and real chirp: ', np.round(mean_match, 3) * 100, '%')
        return float(np.round(mean_match, 3) * 100)

    except ZeroDivisionError:
        # print("Warning: audio too weak or noisy — returning 0% match")
        return 0.0
    except Exception as e:
        # print(f"Error comparing {wav_file_mimic} to {wav_file_real}: {e}")
        return 0.0



def get_player_name(wav_file_path):
    """Extract player name from WAV filename: everything except last 2 underscore-separated parts."""
    base = os.path.basename(wav_file_path)
    name_part = os.path.splitext(base)[0]
    name_segments = name_part.split("_")[:-2]
    player_name = " ".join(name_segments)
    return player_name


def run_comparison(wav_file, real_wav):
    """Run the comparison and return a dictionary with name and score."""
    score = compare_mimic(wav_file, real_wav)
    player_name = get_player_name(wav_file)
    result = {"name": player_name, "score": score}
    return result


def main():
    parser = argparse.ArgumentParser(description="Compare a mimic WAV file to the real chirp")
    parser.add_argument("wav_file", help="Path to the mimic .wav file")
    parser.add_argument("--real_wav", default="recordings/real_chirp/GW150914_L1_shiftedslower.wav",
                        help="Path to the real chirp .wav file")
    args = parser.parse_args()

    result = run_comparison(args.wav_file, args.real_wav)
    print(result)
    return result


if __name__ == "__main__":
    main()
