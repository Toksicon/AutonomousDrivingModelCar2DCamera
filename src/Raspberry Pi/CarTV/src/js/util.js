
export function bytesToSize(bytes, fixed=1) {
    const sizes = ['Bytes', 'kB', 'MB', 'GB', 'TB'];
    if (bytes == 1 || bytes == 0) {
        return (bytes + ' Byte');
    }

    var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return (bytes / Math.pow(1024, i)).toFixed(fixed) + ' ' + sizes[i];
};
