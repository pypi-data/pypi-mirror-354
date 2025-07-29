from .globals import supported_audio_file_extensions

def count_audio_files(audio_folder_path, file_extensions=supported_audio_file_extensions):
    """Count the number of audio files in a folder.

    Args:
        audio_folder_path (str): The path to the folder containing the audio files.
        file_extensions (list, optional): A list of file extensions to consider as audio files. Defaults to supported_audio_file_extensions.

    Returns:
        int: The number of audio files in the folder.
    """
    from novus_pytils.files import get_files_by_extension
    files = get_files_by_extension(audio_folder_path, file_extensions)
    return len(files)

def get_audio_files(audio_folder_path, file_extensions=supported_audio_file_extensions):
    """Get a list of audio files in a folder.

    Args:
        audio_folder_path (str): The path to the folder containing the audio files.
        file_extensions (list, optional): A list of file extensions to consider as audio files. Defaults to supported_audio_file_extensions.

    Returns:
        list: A list of audio file paths.
    """
    from novus_pytils.files import get_files_by_extension
    files = get_files_by_extension(audio_folder_path, file_extensions, relative=True)
    return files


def validate_metadata(audio_folder_path, metadata_csv_filename='metadata.csv'):
    import pandas as pd
    import os
    metadata_df = pd.read_csv(os.path.join(audio_folder_path,metadata_csv_filename))

    #check that the audio folder contains the same number of files as the metadata.csv file
    num_audio_files = count_audio_files(audio_folder_path)
    num_metadata_files = len(metadata_df)
    if num_audio_files != num_metadata_files:
        raise ValueError(f"The number of audio files in the audio folder ({num_audio_files}) does not match the number of files in the metadata.csv file ({num_metadata_files})")

    #check that all audio files are in metadata
    audio_files = get_audio_files(audio_folder_path)
    for audio_file in audio_files:
        if audio_file not in metadata_df['filename'].tolist():
            raise ValueError(f"The audio file {audio_file} is not in the metadata.csv file")

    return True