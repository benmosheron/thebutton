const http = require('http')
const hostname = '127.0.0.1'
const port = 3000;

const server = http.createServer((req, res) => {
    if(req.method === "GET"){
        handleTheGet()
        res.statusCode = 200
        res.setHeader('Content-Type', 'text/plain')
        res.end('Button service ready\n')
    }
    if(req.method === "POST"){
        handleThePost()
        res.statusCode = 200
        res.setHeader('Content-Type', 'text/plain')
        res.end('BUTTONED\n')
    }
  });

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`)
});


function handleThePost(){
    console.log("OMG THE BUTTON")
}

let getCount = 0;
function handleTheGet(){
    getCount++
    if(getCount%1 === 0) console.log(`Got ${getCount} gets.`)
}