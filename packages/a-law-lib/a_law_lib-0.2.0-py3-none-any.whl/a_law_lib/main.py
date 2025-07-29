import numpy as np
from scipy.io import wavfile

def a_law_encode(x, A=87.6):
    """
    Apply A-law compression to a signal.

    Parameters:
        x (numpy.ndarray): Input signal (normalized floating-point values).
        A (float): A-law compression parameter, typically 87.6.

    Returns:
        numpy.ndarray: A-law encoded signal.
    """
    x_abs = np.abs(x)
    threshold = 1 / (1 + np.log(A))
    y = np.where(
        x_abs < threshold,
        x_abs * (1 + np.log(A)),
        1 + np.log(x_abs * A) / np.log(1 + np.log(A))
    )
    return np.sign(x) * y


def a_law_decode(y, A=87.6):
    """
    Decode a signal that was A-law compressed.

    Parameters:
        y (numpy.ndarray): A-law encoded signal.
        A (float): A-law compression parameter used during encoding.

    Returns:
        numpy.ndarray: Decoded (reconstructed) signal.
    """
    y_abs = np.abs(y)
    threshold = 1 / (1 + np.log(A))
    x = np.where(
        y_abs < threshold,
        y_abs / (1 + np.log(A)),
        np.exp((y_abs - 1) * np.log(1 + np.log(A))) / A
    )
    return np.sign(y) * x


def quantize(y, levels=15):
    """
    Perform uniform quantization on the input signal.

    Parameters:
        y (numpy.ndarray): Input signal (typically A-law encoded).
        levels (int): Number of quantization levels.

    Returns:
        tuple:
            - quantized_y (numpy.ndarray): Quantized signal.
            - levels_array (numpy.ndarray): Array of quantization level values.
    """
    max_val = np.max(y)
    min_val = np.min(y)
    step_size = (max_val - min_val) / (levels - 1)
    quantized_y = np.round((y - min_val) / step_size) * step_size + min_val
    return quantized_y, np.linspace(min_val, max_val, levels)


def process_wave_file(input_path, output_path, A=87.6, quant_levels=15):
    """
    Process a WAV file by applying A-law compression, quantization,
    and A-law decoding, then saving the result to a new file.

    Parameters:
        input_path (str): Path to the input WAV file.
        output_path (str): Path to save the processed WAV file.
        A (float): A-law compression parameter.
        quant_levels (int): Number of quantization levels.

    Returns:
        None
    """
    sample_rate, data = wavfile.read(input_path)

    # Normalize if data is integer type (common in wav)
    if data.dtype.kind in 'iu':
        max_val = np.iinfo(data.dtype).max
        data_norm = data.astype(np.float32) / max_val
    else:
        data_norm = data.astype(np.float32)

    # If stereo, process each channel separately
    if data_norm.ndim == 2:
        channels = []
        for ch in range(data_norm.shape[1]):
            y = a_law_encode(data_norm[:, ch], A)
            q, _ = quantize(y, quant_levels)
            x_rec = a_law_decode(q, A)
            channels.append(x_rec)
        processed = np.stack(channels, axis=1)
    else:
        y = a_law_encode(data_norm, A)
        q, _ = quantize(y, quant_levels)
        processed = a_law_decode(q, A)

    # Denormalize to original integer range
    if data.dtype.kind in 'iu':
        processed_int = np.clip(processed * max_val, -max_val, max_val - 1).astype(data.dtype)
    else:
        processed_int = processed.astype(data.dtype)

    wavfile.write(output_path, sample_rate, processed_int)
