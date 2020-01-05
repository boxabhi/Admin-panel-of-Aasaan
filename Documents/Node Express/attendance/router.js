const router = require('express').Router();
var bodyParser = require('body-parser');
const express = require('express')
const app = express()


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



router.get('/', function(req,res){
    res.send('.');
})

router.get('/register'), function(req,res){
    res.send('......!');
    // const username = req.body.username;
    // const password = req.body.password;
    // var sql = `INSERT INTO user (username,password) VALUES ('${username}','${password}')`
   
    
    // connection.query(sql,[username],function (error, results, fields) {
    //       if (error){
    //         res.send({"status":400,"failed":"Error ocurred or User Already exist!"
    //           })
    //       };

    //       res.send({"status":200,"success":"Account Created"});
    //     });
    
}


module.exports = router;
