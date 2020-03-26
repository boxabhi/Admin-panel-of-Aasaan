const express = require('express')
const app = express()
var bodyParser = require('body-parser');
var simplecrypt = require("simplecrypt");
const port = 4000

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
  
  var sc = simplecrypt();
  
  connection.connect(function(err) {
    if (err) console.log(err);
    console.log('You are now connected...')
  })


app.get('/', (req, res) => res.send('Hello Abhijeet'))

app.post('/register',function(req, res){ 
    var username = req.body.username;
    var password = req.body.password;
    const hash = sc.encrypt(password);

    var sql = `INSERT INTO user (username,password) VALUES ('${username}','${password}')`
    
    connection.query(sql,[username],function (error, results, fields) {
      if (error){ 
        console.log("error ocurred",error);
        res.send({"status":400,"failed":"Error ocurred or User Already exist!"});
      };

      res.send({"status":200,"success":"Account Created"});
    });

});

app.post('/login', function(req,res){
    var username = req.body.username;
    var password = (req.body.password);
   // console.log(password);
    var hash = sc.encrypt(password);
    var dhash = sc.decrypt(hash);
    console.log(hash);
 //   console.log(username)
    var sql = `SELECT username from user WHERE username = ${username} `;
    connection.query('SELECT * FROM user WHERE username = ?',[username], function(error,results,fields){
      if (error) {
      res.send({"status":400,"failed":"error ocurred"})
      }else{
        if(results.length > 0){
          if(results[0].password == password){
            res.send({"status":200,"success":'Login Successfull'});
          }
          else{
            res.send({"status":400,"success":'Incorrect Password'});
          }
        }
      }     
    });
})


app.post('/class/', function(req,res){
  
  var subject_name = req.body.subject_name;
  var user_id = req.body.user_id;
  var teacher_name= req.body.teacher_name;
  var class_name = req.body.class;
  console.log(req.body);
  var sql = `INSERT INTO subject (subject_name,teacher_name,class,user_id) VALUES ('${subject_name}','${teacher_name}','${class_name}','${user_id}')`

  connection.query(sql,[subject_name,teacher_name,user_id],function(error,results,fields){
    if (error) {
      res.send({"status":400,"failed":"error ocurred"})
      }else{
        res.send({"status":200,"success":"Class created!"})
      }
  })  
})

app.get('/classes', function(req,res){
  var sql = 'SELECT * FROM CLASSES';
  connection.query(sql, function(err,results,fields){
    if(err){
      res.send({"status":400,"failed":"error ocurred"});
    }else{
      res.send(results)
    }
  })
})

app.get('/students', function(req,res){
  var sql = 'SELECT * FROM students';
  connection.query(sql, function(err,results,fields){
    if(err){
      res.send({"status":400,"failed":"error ocurred"});
    }else{
      res.send(results)
    }
  })
})



app.listen(port, () => console.log(`Express running ${port}!`))