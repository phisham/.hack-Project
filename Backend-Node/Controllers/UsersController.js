const express = require('express')
const router = express.Router();
const bcrypt = require('bcryptjs');
const userServices=require('../Services/UserService');
const multer=require('multer');
const {Needy}=require('../Modals/UsersModel');

var storage = multer.diskStorage({
   destination: function (req, file, cb) {
      cb(null, './uploads');
   },
   filename: (req, file, cb) => {
    cb(null, file.fieldname + "-" + Date.now() + "-" + file.originalname)
 }

});
var upload = multer({ storage: storage });
// handle single file upload
router.post('/upload-file',async(req, res, next) => {
   
     const {
        name,
        number,
        email,
        income,
        location,
        image
        
    } = req.body;
  console.log(req.body.name);

  try {
    await Needy.create({
        name,
        number,
        email,
        income,
        location,
        image
    });
    const db=await Needy.find({});
    console.log(db);
    return res.json({ status: "ok", msg: "Organisation successfully created"});
  } catch (e) {
    return res.json({ status: "error", error: e });
  }

   
});
router.post('/register', (req, res, next) => {
    const {password} = req.body
    const salt = bcrypt.genSaltSync(10);
    req.body.password = bcrypt.hashSync(password, salt);

    userServices.register(req.body).then(
        () => res.send('success')
    ).catch(
        err => next(err)
    )
})

router.get('/details',async(req,res) => {
  try{
    const orgs= await Needy.find({});
    return res.json({ status: "ok", details:orgs });
} catch (e) {
  return res.json({ status: "error", error: e });
}
  
})

router.post('/login', (req, res, next) => {
    const { username, password} = req.body;
    userServices.login({ username, password})
        .then(user => {
            res.json(user)
        }
    ).catch(err => next(err))
})

router.get('/:id', (req, res, next) => {
    userServices.getById(req.params.id).then(
        (user) => res.json(user)
    ).catch(err => next(err))
})


module.exports = router;