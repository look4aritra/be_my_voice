var express = require('express');
var router = express.Router();

var API_KEY = '38b178162f2e497cb564c6a6dafc6c9a';
var newsAPI = require('newsapi');
var news = new newsAPI(API_KEY);

var fs = require('fs');
var dateFormat = require('dateformat');

/* GET news listing. */
router.get('/', function(req, res, next) {
  console.log(req);
  res.send('>_<');
});

/* search news listing. */
router.get('/search', function(req, res, next) {
  console.log(req.query.keyword);
  var searchResult = {keyword: req.query.keyword};
  var timestamp = dateFormat(new Date(), 'yyyymmddHHMMssL');
  news.v2.everything(
    {q: req.query.keyword, pageSize: 100, sortBy: 'relevancy'},
    (err, resp) => {
      if (err) {
        searchResult['count'] = 0;
        res.send(searchResult);
      } else {
        console.log('writing to file');
        var filePath =
          'C:\\Users\\Pratim\\Desktop\\dump\\' +
          timestamp +
          '-' +
          req.query.keyword +
          '.json';
        fs.writeFile(filePath, JSON.stringify(resp), () => {
          console.log('written to file');
          searchResult['count'] = resp.articles.length;
          searchResult['data'] = resp;
          searchResult['file'] = filePath;
          res.send(searchResult);
        });
      }
    }
  );
});

module.exports = router;
