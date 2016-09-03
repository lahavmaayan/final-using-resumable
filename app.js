var express = require('express');
var resumable = require('./resumable-node.js')('/tmp/resumable.js/');

var passport = require('passport');

var GoogleStrategy = require('passport-google-oauth20').Strategy;
var PORT = 8080;

// Configure the Facebook strategy for use by Passport.
//
// OAuth 2.0-based strategies require a `verify` function which receives the
// credential (`accessToken`) for accessing the Facebook API on the user's
// behalf, along with the user's profile.  The function must invoke `cb`
// with a user object, which will be set at `req.user` in route handlers after
// authentication.
passport.use(new GoogleStrategy({
        clientID: '724606193534-b6c32gs1b5jppkh3mur4gtq1rkflei4v.apps.googleusercontent.com',
        clientSecret: 's30j64irYutAWMZ-26Tps5_y',
        callbackURL: 'http://localhost:8080/login/google/return'
    },
    function(accessToken, refreshToken, profile, cb) {
        // In this example, the user's Facebook profile is supplied as the user
        // record.  In a production-quality application, the Facebook profile should
        // be associated with a user record in the application's database, which
        // allows for account linking and authentication with other identity
        // providers.

        // console.log('***************************************');
        // console.log(profile);
        // console.log(accessToken);
        // console.log(refreshToken);
        // console.log(cb);

        return cb(null, profile);
    }));


// Configure Passport authenticated session persistence.
//
// In order to restore authentication state across HTTP requests, Passport needs
// to serialize users into and deserialize users out of the session.  In a
// production-quality application, this would typically be as simple as
// supplying the user ID when serializing, and querying the user record by ID
// from the database when deserializing.  However, due to the fact that this
// example does not have a database, the complete Twitter profile is serialized
// and deserialized.
passport.serializeUser(function(user, cb) {
    // console.log('***************************************');
    // console.log('serializeUser');
    // console.log(user);
    cb(null, user);
});

passport.deserializeUser(function(obj, cb) {
    // console.log('***************************************');
    // console.log('DEserializeUser');
    // console.log(obj);
    cb(null, obj);
});




var app = express();
var multipart = require('connect-multiparty');



var morgan = require('morgan');
//middleware, will record everything in the dev env.


var PORT = 8080;

var cookieParser = require('cookie-parser');
var session = require('express-session');
var passport = require('passport');
var flash = require('connect-flash');
var bodyParser =require('body-parser');

app.use(require('cookie-parser')());
app.use(require('body-parser').urlencoded({
    extended: true
}));
app.use(require('express-session')({
    secret: 'keyboard cat',
    resave: true,
    saveUninitialized: true
}));

// Initialize Passport and restore authentication state, if any, from the
// session.
app.use(passport.initialize());
app.use(passport.session());



app.use(morgan('dev'));
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
// app.use(cookieParser());
// app.use(bodyParser.urlencoded({extended: true}));
// app.use(session({secret: 'anystringoftext'}));

// app.use(passport.initialize());
// app.use(passport.session());
// app.use(flash());

// app.set('view engine', 'ejs');

// Host most stuff in the public folder
app.use(express.static(__dirname + '/public'));

app.use(multipart());

// passport.serializeUser(function(user, done){
//   done(null, user._id);
// });
// passport.deserializeUser(function(id, done){
//   User.findById(id, function(err, user){
//     done(err, user);
//   });
// });
app.get('/', function(req, res){
  res.render('home', {
            user: req.user
        });
});
// Uncomment to allow CORS
// app.use(function (req, res, next) {
//    res.header('Access-Control-Allow-Origin', '*');
//    next();
// });
// app.get('/home', function(req, res){
//   res.render('home', {
//             user: req.user
//         });
// });

app.get('/login',
    function(req, res) {
        res.render('login');
    });

app.get('/login/google',
    passport.authenticate('google', {
        scope: ['profile']
    }));

app.get('/login/google/return',
    passport.authenticate('google', {
        failureRedirect: '/login'
    }),
    function(req, res) {
        res.redirect('/');
    });


app.get('/profile',
    require('connect-ensure-login').ensureLoggedIn(),
    function(req, res) {
        // console.log('***************************************');
        // console.log('/profile');
        // console.log(req.user);
        res.render('profile', {
            user: req.user
        });
    });

app.get('/uploadJson',
  require('connect-ensure-login').ensureLoggedIn(),
  function(req, res) {

    var id = req.user.id;
    resumable.changeDir('./users/' + id);
    
    res.sendFile(__dirname + '/public/bindex.html');
});

// Handle uploads through Resumable.js
app.post('/upload', function(req, res){
    resumable.post(req, function(status, filename, original_filename, identifier){
        console.log('POST', status, original_filename, identifier);

        res.send(status);
    });
});

// Handle status checks on chunks through Resumable.js
app.get('/upload', function(req, res){
    resumable.get(req, function(status, filename, original_filename, identifier){
        console.log('GET', status);
        res.send((status == 'found' ? 200 : 404), status);
    });
});

app.get('/download/:identifier', function(req, res){
	resumable.write(req.params.identifier, res);
});
app.get('/resumable.js', function (req, res) {
  // console.log(req.cookies);
	// console.log('================');
	// console.log(req.session);
  // console.log('in resumable');
  // console.log('this is the req.user:');
  // console.log(req.user);
  var fs = require('fs');
  res.setHeader("content-type", "application/javascript");
  fs.createReadStream("../../resumable.js").pipe(res);
});

app.listen(PORT, function(){
  console.log('app is listening on port - ' + PORT);
});
