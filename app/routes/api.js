var express = require('express');
var router = express.Router();
var dataController = require('../controllers/dataController');

/* GET home page. */
router.get('/data', dataController.getData);


module.exports = router;
