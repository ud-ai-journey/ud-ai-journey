import os
import shutil # Used for moving files

def organize_directory(target_directory):
    """
    Organizes files in a given directory into subfolders based on file type.

    Args:
        target_directory (str): The path to the directory to organize.
    """
    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        return

    print(f"Starting organization of directory: {target_directory}")

    # Define mappings of file extensions to folder names
    # Add more mappings as needed! (use lowercase extensions)
    extension_mapping = {
        # Documents
        '.txt': 'Documents', '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
        '.odt': 'Documents', '.rtf': 'Documents', '.tex': 'Documents', '.wpd': 'Documents',
        '.md': 'Documents', '.ppt': 'Documents', '.pptx': 'Documents', '.xls': 'Documents',
        '.xlsx': 'Documents', '.csv': 'Documents',

        # Images
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
        '.bmp': 'Images', '.tiff': 'Images', '.webp': 'Images', '.svg': 'Images',
        '.ico': 'Images',

        # Audio
        '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio', '.aac': 'Audio',
        '.ogg': 'Audio', '.wma': 'Audio', '.m4a': 'Audio',

        # Video
        '.mp4': 'Videos', '.mov': 'Videos', '.avi': 'Videos', '.mkv': 'Videos',
        '.wmv': 'Videos', '.flv': 'Videos', '.webm': 'Videos', '.mpeg': 'Videos',
        '.mpg': 'Videos',

        # Archives
        '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives', '.tar': 'Archives',
        '.gz': 'Archives', '.bz2': 'Archives', '.xz': 'Archives',

        # Executables / Installers
        '.exe': 'Executables', '.msi': 'Executables', '.deb': 'Executables', '.rpm': 'Executables',
        '.pkg': 'Executables', '.dmg': 'Executables',

        # Code / Scripts
        '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code', '.json': 'Code',
        '.xml': 'Code', '.c': 'Code', '.cpp': 'Code', '.java': 'Code', '.sh': 'Code',
        '.bat': 'Code', '.ps1': 'Code', '.vbs': 'Code', '.php': 'Code', '.rb': 'Code',
        '.go': 'Code', '.swift': 'Code', '.kt': 'Code', '.ts': 'Code',

        # Spreadsheets (already covered in Documents, but good to list explicitly if needed)
        # '.xls': 'Spreadsheets', '.xlsx': 'Spreadsheets', '.csv': 'Spreadsheets',

        # Presentations (already covered in Documents, but good to list explicitly if needed)
        # '.ppt': 'Presentations', '.pptx': 'Presentations',

        # Fonts
        '.ttf': 'Fonts', '.otf': 'Fonts', '.woff': 'Fonts', '.woff2': 'Fonts',

        # Disk Images
        '.iso': 'Disk Images', '.img': 'Disk Images', '.vmdk': 'Disk Images', '.vhd': 'Disk Images',

        # Databases
        '.sql': 'Databases', '.db': 'Databases', '.sqlite': 'Databases',
    }

    # Iterate over all items in the directory
    for item_name in os.listdir(target_directory):
        # Construct the full path to the item
        item_path = os.path.join(target_directory, item_name)

        # Skip if it's a directory (we only want to organize files)
        if os.path.isdir(item_path):
            print(f"Skipping directory: {item_name}")
            continue

        # Skip the script file itself if it's in the target directory
        if item_name == os.path.basename(__file__):
             print(f"Skipping script file: {item_name}")
             continue

        # Get the file extension (lowercase)
        # os.path.splitext returns (root, ext)
        _, file_extension = os.path.splitext(item_name)
        file_extension = file_extension.lower() # Ensure lowercase for mapping lookup

        # Determine the destination folder name
        # Use '.no_extension' as a key for files without extensions
        if file_extension == "":
             destination_folder_name = extension_mapping.get('.no_extension', 'Others')
        else:
             destination_folder_name = extension_mapping.get(file_extension, 'Others')

        # Construct the path for the destination folder
        destination_folder_path = os.path.join(target_directory, destination_folder_name)

        # Create the destination folder if it doesn't exist
        # exist_ok=True prevents errors if the folder already exists
        os.makedirs(destination_folder_path, exist_ok=True)

        # Construct the full destination path for the file
        destination_file_path = os.path.join(destination_folder_path, item_name)

        # Handle potential file name collisions (simple version: skip)
        if os.path.exists(destination_file_path):
            print(f"Skipping (duplicate): {item_name} -> {destination_folder_name}")
            # For a more robust solution, you could rename the file like item_name(1).ext
            continue

        # Move the file to the destination folder
        try:
            shutil.move(item_path, destination_file_path)
            print(f"Moved: {item_name} -> {destination_folder_name}")
        except Exception as e:
            print(f"Error moving {item_name}: {e}")


# --- Main execution block ---
if __name__ == "__main__":
    # You can hardcode a path here for convenience during testing
    # target_dir = "/path/to/your/messy/folder" # Uncomment and replace!

    # Or prompt the user to enter the path
    target_dir = input("Enter the path to the directory you want to organize: ")

    # Expand user home directory symbol (like ~)
    target_dir = os.path.expanduser(target_dir)

    organize_directory(target_dir)
    print("\nOrganization complete.")