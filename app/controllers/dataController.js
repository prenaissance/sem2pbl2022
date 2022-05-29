const {spawn} = require('child_process');

exports.getData = (req, res) => {
  const {age, education, maritalStatus, occupation, hours} = req.query;

  const pythonProcess = spawn('python', ['./handlers/data/randomForest.py', age, education, maritalStatus, occupation, hours]);
  pythonProcess.stdout.on("data", (data) => {
    console.log(data);
    res.json({
      result: data === "1" ? true : false
    });
  });

  pythonProcess.on("error", (err) => {
    console.log(`spawn process error ${err}`);
  });
  
  pythonProcess.stderr.on("data", (err) => {
    console.log(`spawn process stderr ${err}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
  });

}
