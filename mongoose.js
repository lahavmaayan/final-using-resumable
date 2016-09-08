var mongoose = require('mongoose');

module.exports = mongoose.model('User', {
  usename: String,
  password: String,
  email: String
});

// module.exports = {
//   'model': {mongoose.model('User', {
//     username:String,
//     password: String,
//     email: String
//   })},
//   'url': 'mongodb://finalProj:finalProj@ds019826.mlab.com:19826/final-proj'
//
// };
