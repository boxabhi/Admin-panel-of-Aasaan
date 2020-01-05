
var mysql = require('mysql')
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'attendance'
  })

  app.use(bodyParser.urlencoded({ 
    extended: false
  }));
  app.use(bodyParser.json());
  app.use(bodyParser.text({ type: 'text/html' }))
  app.use(bodyParser.text({ type: 'text/xml' }))
  app.use(bodyParser.raw({ type: 'application/vnd.custom-type' }))
  app.use(bodyParser.json({ type: 'application/*+json' }))
  

  
  connection.connect(function(err) {
    if (err) console.log(err);
    console.log('You are now connected...')
  })


