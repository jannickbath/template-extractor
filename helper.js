const fs = require('fs');

function copyFile(src, dest) {
    fs.copyFileSync(src, dest);
}

function createDir(path, options = { recursive: false }) {
    fs.mkdirSync(path, options);
}

function createFile(path) {
    fs.writeFileSync(path, '');
}

function searchAndReplaceFileContentsRegex(path, regex, replaceString) {
    let content = fs.readFileSync(path, 'utf8');
    content = content.replace(new RegExp(regex, 'g'), replaceString);
    fs.writeFileSync(path, content);
}

function appendStringToFile(path, string) {
    fs.appendFileSync(path, string);
}

function prependStringToFile(path, string) {
    let content = fs.readFileSync(path, 'utf8');
    content = string + content;
    fs.writeFileSync(path, content);
}

function searchAndReplaceFileContents(path, matchString, replaceString) {
    let content = fs.readFileSync(path, 'utf8');
    content = content.replace(matchString, replaceString);
    fs.writeFileSync(path, content);
}

function deletePath(path) {
    if (fs.existsSync(path)) {
        if (fs.lstatSync(path).isDirectory()) {
            fs.rmdirSync(path, { recursive: true });
        } else {
            fs.unlinkSync(path);
        }
    }
}

function listFiles(directory) {
    return fs.readdirSync(directory).filter(file => fs.lstatSync(file).isFile());
}

function readFileContents(path) {
    return fs.readFileSync(path, 'utf8');
}

function writeFile(path, content) {
    fs.writeFileSync(path, content);
}

function exists(path) {
    return fs.existsSync(path);
}

function rename(oldPath, newPath) {
    fs.renameSync(oldPath, newPath);
}

function getFileSize(path) {
    const stats = fs.statSync(path);
    return stats.size;
}

function moveFile(src, dest) {
    fs.renameSync(src, dest);
}

// Export the functions
module.exports = {
    copyFile,
    createDir,
    createFile,
    searchAndReplaceFileContentsRegex,
    appendStringToFile,
    prependStringToFile,
    searchAndReplaceFileContents,
    deletePath,
    listFiles,
    readFileContents,
    writeFile,
    exists,
    rename,
    getFileSize,
    moveFile
};
