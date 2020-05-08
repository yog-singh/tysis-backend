var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var multer = require('multer');
const spawn = require("child_process").spawn;

//var indexRouter = require('./routes/index');
//var usersRouter = require('./routes/users');

var app = express();

// view engine setup

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

const uploading = multer({
  dest: __dirname + '/public/images/'
});

app.post('/upload', uploading.single('image'), function (req, res, next) {
  if (req.file) {
    var datad;
    const pythonProcess = spawn('python',[`${__dirname}/public/script/pyts.py`, `${__dirname}/public/images/${req.file.filename}`]);
    pythonProcess.stdout.on("data", (data) => {
      datad = data.toString();
    });
    pythonProcess.on("close", (code) => {
      res.status(200).json({
        "message": datad
      });
    });
  }
  //console.log(__dirname + "/public/images/" + req.file.filename);
});
//app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.json({
    "error": err
  });
});

app.listen(8182, () => { 
  console.log('Listening on 8080.');
})