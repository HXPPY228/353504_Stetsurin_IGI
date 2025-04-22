import zipfile

class FileManager:
    """Class for managing file operations: reading, writing, and archiving."""
    
    @staticmethod
    def read_file(filename):
        """
        Read the content of the file.
        
        Args:
            filename (str): The name of the file to read.
        
        Returns:
            str: The content of the file.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    @staticmethod
    def write_file(filename, content):
        """
        Write the content to the file.
        
        Args:
            filename (str): The name of the file to write to.
            content (str): The content to write.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Data successfully written to '{filename}'.")
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    @staticmethod
    def archive_file(filename, archive_name):
        """
        Archive the file using zip.
        
        Args:
            filename (str): The name of the file to archive.
            archive_name (str): The name of the archive.
        """
        try:
            with zipfile.ZipFile(archive_name, 'w') as zipf:
                zipf.write(filename)
            print(f"File '{filename}' archived to '{archive_name}'.")
        except Exception as e:
            print(f"Error archiving file: {e}")
    
    @staticmethod
    def get_archive_info(archive_name):
        """
        Get information about the files in the archive.
        
        Args:
            archive_name (str): The name of the archive.
        
        Returns:
            list: List of file information in the archive.
        """
        try:
            with zipfile.ZipFile(archive_name, 'r') as zipf:
                return zipf.infolist()
        except Exception as e:
            print(f"Error getting archive info: {e}")
            return []
