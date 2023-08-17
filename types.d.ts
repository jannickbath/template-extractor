declare module 'helper' {
    /**
     * Copies a file from source to destination.
     * @param src - Source path of the file.
     * @param dest - Destination path for the copied file.
     */
    export function copyFile(src: string, dest: string): void;

    /**
     * Creates a directory. Can create nested directories if specified.
     * @param path - Path of the directory to be created.
     * @param options - Options for directory creation. Set `recursive` to true for nested directories.
     */
    export function createDir(path: string, options?: { recursive?: boolean }): void;

    /**
     * Creates an empty file at the specified path.
     * @param path - Path where the file should be created.
     */
    export function createFile(path: string): void;

    /**
     * Searches for a pattern in a file and replaces it.
     * Uses regex for search.
     * @param path - Path of the file.
     * @param regex - Regular expression pattern or string to search for.
     * @param replaceString - String that replaces the matched pattern.
     */
    export function searchAndReplaceFileContentsRegex(path: string, regex: string | RegExp, replaceString: string): void;

    /**
     * Appends a string to the end of a file.
     * @param path - Path of the file.
     * @param string - String to append.
     */
    export function appendStringToFile(path: string, string: string): void;

    /**
     * Prepends a string to the beginning of a file.
     * @param path - Path of the file.
     * @param string - String to prepend.
     */
    export function prependStringToFile(path: string, string: string): void;

    /**
     * Searches for a substring in a file and replaces it.
     * @param path - Path of the file.
     * @param matchString - Substring to search for.
     * @param replaceString - String that replaces the matched substring.
     */
    export function searchAndReplaceFileContents(path: string, matchString: string, replaceString: string): void;

    /**
     * Deletes a file or directory. If a directory, deletes it recursively.
     * @param path - Path of the file or directory.
     */
    export function deletePath(path: string): void;

    /**
     * Lists all files in a directory.
     * @param directory - Path of the directory.
     * @returns Array of filenames.
     */
    export function listFiles(directory: string): string[];

    /**
     * Reads and returns the content of a file.
     * @param path - Path of the file.
     * @returns Content of the file.
     */
    export function readFileContents(path: string): string;

    /**
     * Writes content to a file. Overwrites the file if it already exists.
     * @param path - Path of the file.
     * @param content - Content to write.
     */
    export function writeFile(path: string, content: string): void;

    /**
     * Checks if a file or directory exists.
     * @param path - Path to check.
     * @returns True if exists, false otherwise.
     */
    export function exists(path: string): boolean;

    /**
     * Renames a file or directory.
     * @param oldPath - Current path of the file or directory.
     * @param newPath - New path for the file or directory.
     */
    export function rename(oldPath: string, newPath: string): void;

    /**
     * Returns the size of a file in bytes.
     * @param path - Path of the file.
     * @returns Size of the file in bytes.
     */
    export function getFileSize(path: string): number;

    /**
     * Moves a file from source to destination.
     * @param src - Source path of the file.
     * @param dest - Destination path for the moved file.
     */
    export function moveFile(src: string, dest: string): void;
}
