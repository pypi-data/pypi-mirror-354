from globals import supported_audio_file_extensions
from novus_pytils.files import get_files_by_extension

def count_audio_files(audio_folder_path, file_extensions=supported_audio_file_extensions):
    files = get_files_by_extension(audio_folder_path, file_extensions)
    return len(files)
