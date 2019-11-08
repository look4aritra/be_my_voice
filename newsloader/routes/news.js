var express = require('express');
var router = express.Router();

var API_KEY = '';

/* GET news listing. */
router.get('/', function(req, res, next) {
  console.log(req);
  res.send('>_<');
});

/* search news listing. */
router.get('/search', function(req, res, next) {
  console.log(req);
  res.send({count: 1, location: ''});
});

module.exports = router;
