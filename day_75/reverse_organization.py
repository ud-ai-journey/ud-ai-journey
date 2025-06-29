import os
import shutil

def reverse_organization(target_directory):
    """
    Moves all files from subdirectories back to the parent directory.
    """
    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        return

    print(f"Starting to reverse organization in: {target_directory}")
    
    # List of common folder names created by the organizer
    common_folders = [
        'Documents', 'Images', 'Audio', 'Videos', 'Archives',
        'Executables', 'Code', 'Fonts', 'Disk Images', 'Databases', 'Others'
    ]
    
    moved_count = 0
    skipped_count = 0
    error_count = 0
    
    # Get list of all items in the target directory
    for item in os.listdir(target_directory):
        item_path = os.path.join(target_directory, item)
        
        # Only process directories that match our common folders
        if os.path.isdir(item_path) and item in common_folders:
            print(f"Processing folder: {item}")
            
            # Move each file from the subfolder to the parent
            for root, _, files in os.walk(item_path):
                for file in files:
                    src = os.path.join(root, file)
                    dst = os.path.join(target_directory, file)
                    
                    # Handle potential filename conflicts
                    if os.path.exists(dst):
                        print(f"  Skipping (already exists): {file}")
                        skipped_count += 1
                        continue
                        
                    try:
                        shutil.move(src, dst)
                        print(f"  Moved back: {file}")
                        moved_count += 1
                    except Exception as e:
                        print(f"  Error moving {file}: {e}")
                        error_count += 1
            
            # Remove the now-empty directory
            try:
                os.rmdir(item_path)
                print(f"Removed empty folder: {item}")
            except Exception as e:
                print(f"Could not remove folder {item}: {e}")
    
    print("\nReversal complete!")
    print(f"Files moved back: {moved_count}")
    print(f"Files skipped (already existed): {skipped_count}")
    print(f"Errors encountered: {error_count}")

if __name__ == "__main__":
    target_dir = input("Enter the path to the directory you want to reverse organization for: ")
    target_dir = os.path.expanduser(target_dir)
    reverse_organization(target_dir)
