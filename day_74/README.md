# Day 74: File Organizer and Reversal Tool

## 📂 Project Overview
This project consists of two Python scripts that work together to help manage files:
1. `file_organizer.py` - Organizes files into categorized folders based on their extensions
2. `reverse_organization.py` - Reverses the organization by moving files back to their original location

## 🛠️ Features

### File Organizer (`file_organizer.py`)
- Organizes files into categorized folders (Documents, Images, Videos, etc.)
- Handles a wide variety of file extensions
- Skips directories and the script itself
- Prevents file overwrites
- Provides clear console output of all actions

### Reversal Tool (`reverse_organization.py`)
- Moves files back to their original parent directory
- Handles potential filename conflicts
- Removes empty folders after moving files
- Provides a summary of actions taken

## 📋 Supported File Categories
- **Documents**: .pdf, .docx, .txt, .pptx, .xlsx, etc.
- **Images**: .jpg, .png, .gif, .svg, etc.
- **Audio**: .mp3, .wav, .flac, etc.
- **Videos**: .mp4, .mov, .avi, etc.
- **Archives**: .zip, .rar, .7z, etc.
- **Executables**: .exe, .msi, .dmg, etc.
- **Code**: .py, .js, .html, .css, etc.
- **Fonts**: .ttf, .otf, .woff, etc.
- **Disk Images**: .iso, .img, etc.
- **Databases**: .sql, .db, etc.
- **Others**: Any file not matching the above categories

## 🚀 How to Use

### Organizing Files
1. Run the script:
   ```
   python file_organizer.py
   ```
2. Enter the path to the directory you want to organize when prompted
   Example: `C:\Users\YourUsername\Desktop`

### Reversing the Organization
1. Run the reversal script:
   ```
   python reverse_organization.py
   ```
2. Enter the path to the directory where you want to reverse the organization

## ⚠️ Important Notes
- The organizer will skip files that would overwrite existing files
- The reversal tool will not overwrite files that already exist in the target directory
- Both scripts provide detailed output of their actions
- The organizer creates folders as needed in the target directory

## 🛠️ Requirements
- Python 3.x
- No additional packages required (uses only standard library modules)

## 📝 Example Usage

### Organizing Files
```
> python file_organizer.py
Enter the path to the directory you want to organize: C:\Users\Example\Desktop
Starting organization of directory: C:\Users\Example\Desktop
Moved: example.pdf -> Documents
Moved: photo.jpg -> Images
...
Organization complete.
```

### Reversing Organization
```
> python reverse_organization.py
Enter the path to the directory you want to reverse organization for: C:\Users\Example\Desktop
Starting to reverse organization in: C:\Users\Example\Desktop
Processing folder: Documents
  Moved back: example.pdf
Processing folder: Images
  Moved back: photo.jpg
...
Reversal complete!
Files moved back: 15
Files skipped (already existed): 0
Errors encountered: 0
```

## 📜 License
This project is open source and available under the MIT License.

## ✍️ Author

Boya Uday Kumar  

*   Built with ❤️ during the **100-Day AI Build Challenge**.

---

## 💬 Contact

Reach out on GitHub or connect via [Portfolio](https://ud-ai-kumar.vercel.app/) to collaborate on educational AI projects.