const glob = require('glob')
const fs = require('fs')


let path = process.argv[2]
let begin = process.argv[3]
let end = process.argv[4]
let files = findCSVFiles()
console.log(`FILES: ${files}`)
let writeStream = fs.createWriteStream('dosya.csv')
let promises = files.map((f, i) => {
    readFile(f, begin, end, l => writeStream.write(l + "\n"))
})
Promise.all(promises).then(writeStream.on("finish", () => writeStream.end()))

function findCSVFiles() {
    return glob.sync(`${path}/.log.*`)
}

async function readFile(file, begin, end, cb){
    return new Promise((resolve, reject) => {
        let lineReader = require('readline').createInterface({
            input: fs.createReadStream(file)
        })
        let lineCount = 0 
        lineReader.on('line', line => {
            lineCount++
            if (lineCount >= begin && lineCount < end) cb(line)
            if (lineCount == end) {
                lineReader.close()
            }
        })
        lineReader.on('close', () => {
            resolve(1)
        })
    })
};
