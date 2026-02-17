"""File management module for handling file operations and storage.

This module provides abstraction for common file operations including reading,
writing, deletion, and directory management with proper error handling and logging.
"""

import logging
import os
import shutil
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


class FileManager:
    """Manages file operations and directory handling.
    
    Provides methods for reading, writing, deleting, and manipulating files
    and directories with consistent error handling and logging throughout.
    """

    def __init__(self, base_path: str | Path | None = None):
        """Initialize FileManager.
        
        Args:
            base_path (str | Path | None, optional): Base directory path for relative
                file operations. If None, uses current working directory.
                Defaults to None.
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        
        # Ensure base path exists
        if not self.base_path.exists():
            try:
                self.base_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Base path created: {self.base_path}")
            except Exception as e:
                logger.error(f"Failed to create base path {self.base_path}: {e}")
                raise
        
        logger.info(f"FileManager initialized with base path: {self.base_path}")

    def _resolve_path(self, file_path: str | Path) -> Path:
        """Resolve a file path relative to the base path.
        
        Args:
            file_path (str | Path): The file path to resolve.
            
        Returns:
            Path: Absolute path object.
        """
        path = Path(file_path)
        if not path.is_absolute():
            path = self.base_path / path
        return path.resolve()

    def read_file(self, file_path: str | Path, encoding: str = 'utf-8') -> Optional[str]:
        """Read file contents as text.
        
        Args:
            file_path (str | Path): Path to the file to read.
            encoding (str, optional): File encoding. Defaults to 'utf-8'.
            
        Returns:
            Optional[str]: File contents, or None if read fails.
        """
        try:
            path = self._resolve_path(file_path)
            if not path.exists():
                logger.warning(f"File not found: {path}")
                return None
            
            content = path.read_text(encoding=encoding)
            logger.debug(f"File read successfully: {path}")
            return content
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return None

    def write_file(self, file_path: str | Path, content: str, 
                   encoding: str = 'utf-8', create_dirs: bool = True) -> bool:
        """Write content to a file.
        
        Args:
            file_path (str | Path): Path to the file to write.
            content (str): Content to write to the file.
            encoding (str, optional): File encoding. Defaults to 'utf-8'.
            create_dirs (bool, optional): Create parent directories if needed.
                Defaults to True.
                
        Returns:
            bool: True if write was successful, False otherwise.
        """
        try:
            path = self._resolve_path(file_path)
            
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)
            
            path.write_text(content, encoding=encoding)
            logger.info(f"File written successfully: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            return False

    def append_file(self, file_path: str | Path, content: str, 
                    encoding: str = 'utf-8') -> bool:
        """Append content to a file.
        
        Args:
            file_path (str | Path): Path to the file to append to.
            content (str): Content to append.
            encoding (str, optional): File encoding. Defaults to 'utf-8'.
            
        Returns:
            bool: True if append was successful, False otherwise.
        """
        try:
            path = self._resolve_path(file_path)
            
            with open(path, 'a', encoding=encoding) as f:
                f.write(content)
            
            logger.debug(f"Content appended to file: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to append to file {file_path}: {e}")
            return False

    def delete_file(self, file_path: str | Path) -> bool:
        """Delete a file.
        
        Args:
            file_path (str | Path): Path to the file to delete.
            
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            path = self._resolve_path(file_path)
            
            if not path.exists():
                logger.warning(f"File does not exist: {path}")
                return False
            
            path.unlink()
            logger.info(f"File deleted successfully: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return False

    def file_exists(self, file_path: str | Path) -> bool:
        """Check if a file exists.
        
        Args:
            file_path (str | Path): Path to the file to check.
            
        Returns:
            bool: True if file exists, False otherwise.
        """
        try:
            path = self._resolve_path(file_path)
            exists = path.is_file()
            return exists
        except Exception as e:
            logger.error(f"Error checking file existence for {file_path}: {e}")
            return False

    def create_directory(self, dir_path: str | Path) -> bool:
        """Create a directory and parent directories if needed.
        
        Args:
            dir_path (str | Path): Path to the directory to create.
            
        Returns:
            bool: True if creation was successful, False otherwise.
        """
        try:
            path = self._resolve_path(dir_path)
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created successfully: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {dir_path}: {e}")
            return False

    def delete_directory(self, dir_path: str | Path, recursive: bool = True) -> bool:
        """Delete a directory.
        
        Args:
            dir_path (str | Path): Path to the directory to delete.
            recursive (bool, optional): If True, recursively delete directory contents.
                If False, only delete empty directories. Defaults to True.
                
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            path = self._resolve_path(dir_path)
            
            if not path.exists():
                logger.warning(f"Directory does not exist: {path}")
                return False
            
            if recursive:
                shutil.rmtree(path)
            else:
                path.rmdir()
            
            logger.info(f"Directory deleted successfully: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete directory {dir_path}: {e}")
            return False

    def list_files(self, dir_path: str | Path | None = None, 
                   pattern: str = '*', recursive: bool = False) -> List[Path]:
        """List files in a directory.
        
        Args:
            dir_path (str | Path | None, optional): Directory to list files in.
                If None, uses base path. Defaults to None.
            pattern (str, optional): Glob pattern to filter files.
                Defaults to '*' (all files).
            recursive (bool, optional): If True, recursively search subdirectories.
                Defaults to False.
                
        Returns:
            List[Path]: List of file paths matching the pattern.
        """
        try:
            path = self._resolve_path(dir_path) if dir_path else self.base_path
            
            if not path.exists():
                logger.warning(f"Directory does not exist: {path}")
                return []
            
            if recursive:
                files = list(path.rglob(pattern))
            else:
                files = list(path.glob(pattern))
            
            # Filter to only files (not directories)
            files = [f for f in files if f.is_file()]
            
            logger.debug(f"Found {len(files)} files in {path}")
            return files
        except Exception as e:
            logger.error(f"Failed to list files in {dir_path}: {e}")
            return []

    def copy_file(self, source: str | Path, destination: str | Path, 
                  overwrite: bool = False) -> bool:
        """Copy a file.
        
        Args:
            source (str | Path): Source file path.
            destination (str | Path): Destination file path.
            overwrite (bool, optional): If False, skip if destination exists.
                Defaults to False.
                
        Returns:
            bool: True if copy was successful, False otherwise.
        """
        try:
            src_path = self._resolve_path(source)
            dst_path = self._resolve_path(destination)
            
            if not src_path.exists():
                logger.error(f"Source file does not exist: {src_path}")
                return False
            
            if dst_path.exists() and not overwrite:
                logger.warning(f"Destination file already exists and overwrite=False: {dst_path}")
                return False
            
            # Create parent directory if needed
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(src_path, dst_path)
            logger.info(f"File copied successfully: {src_path} -> {dst_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to copy file from {source} to {destination}: {e}")
            return False

    def rename_file(self, file_path: str | Path, new_name: str) -> bool:
        """Rename a file.
        
        Args:
            file_path (str | Path): Path to the file to rename.
            new_name (str): New file name (without path).
            
        Returns:
            bool: True if rename was successful, False otherwise.
        """
        try:
            path = self._resolve_path(file_path)
            
            if not path.exists():
                logger.error(f"File does not exist: {path}")
                return False
            
            new_path = path.parent / new_name
            path.rename(new_path)
            logger.info(f"File renamed successfully: {path} -> {new_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to rename file {file_path}: {e}")
            return False

    def get_file_size(self, file_path: str | Path) -> Optional[int]:
        """Get the size of a file in bytes.
        
        Args:
            file_path (str | Path): Path to the file.
            
        Returns:
            Optional[int]: File size in bytes, or None if operation fails.
        """
        try:
            path = self._resolve_path(file_path)
            
            if not path.exists():
                logger.warning(f"File does not exist: {path}")
                return None
            
            size = path.stat().st_size
            return size
        except Exception as e:
            logger.error(f"Failed to get file size for {file_path}: {e}")
            return None

    def get_absolute_path(self, file_path: str | Path) -> Optional[str]:
        """Get the absolute path for a given file path.
        
        Args:
            file_path (str | Path): Path to resolve.
            
        Returns:
            Optional[str]: Absolute path as string, or None if operation fails.
        """
        try:
            path = self._resolve_path(file_path)
            return str(path)
        except Exception as e:
            logger.error(f"Failed to resolve path {file_path}: {e}")
            return None
