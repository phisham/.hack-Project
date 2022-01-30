const mongoose = require("mongoose");
const { Schema } = mongoose;

const UserSchema = new Schema({
    username: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
        unique: true,
    },
    password: {
        type: String,
        required: true,
    },
    date: {
        type: Date,
        default: Date.now(),
    },
});

const needy = new Schema(
  {
    name: {
      type: String,
      
    },
    number: {
      type: Number,
      
    },
    email: {
      type: String,
      
    },
    income: {
      type: Number,
      
    },
    location: {
      type: String,
      
    },
    image:{
        type:String,
        
    }
   
  },
  { collection: "needychema", timestamp: true }
);


UserSchema.set('toJSON', {
    transform: (document, returnedObject) => {
        returnedObject.id = returnedObject._id.toString()
        delete returnedObject._id
        delete returnedObject.__v
        //do not reveal passwordHash
        delete returnedObject.password
    }
})

const User =  mongoose.model("user", UserSchema);
const Needy=mongoose.model("needy",needy);
module.exports = {User,Needy};