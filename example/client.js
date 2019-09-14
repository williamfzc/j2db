// before using this, you may need `npm install -g request`
// you can view this site if error happened: https://github.com/request/request/issues/2788
const request = require('request')

var url = 'http://127.0.0.1:9410/api/json/form'
var requestForm = {
    table: 'some_table',
    action: 'insert',
    content: JSON.stringify({
        id: 50000,
        name: "williamfzc",
    })
}

request.post({url: url, form: requestForm}, function (error, response, body) {
    console.log(error)
    console.log(response)
    console.log(body)
})
