
const express = require('express');
const app = express();
const mongoose = require('mongoose');
const auth = require('./Helpers/jwt');
const unless = require('express-unless')
const users = require('./Controllers/UsersController');
const errors = require('./Helpers/ErrorHandler');
const cors = require('cors');
// middleware for authenticating token submitted with requests
auth.authenticateToken.unless = unless
// app.use(auth.authenticateToken.unless({
//     path: [
//         { url: '/users/login', methods: ['POST']},
//         { url: '/users/register', methods: ['POST']},
//         { url:'/users/upload-file',methods:['POST']},
//         { url:'/users/details',methods:['GET']}
//     ]
// }))
app.use(cors());

app.use('./uploads', express.static('uploads'));
app.use(express.json()) // middleware for parsing application/json
app.use('/users', users) // middleware for listening to routes
app.use(errors.errorHandler);

mongoose.connect('mongodb+srv://phisham100:Hisham%4021@cluster0.jmjq8.mongodb.net/Authentication_System?retryWrites=true&w=majority')
.then(console.log("MongoDB connected...."));
 
// get reference to database
var db = mongoose.connection;

db.on('error', console.error.bind(console, 'connection error:'));

const port =process.env.PORT || 9000;
app.listen(port,(req,res)=>{
    console.log("Server started on port 3000");
})