const mongoose = require('mongoose');

const dotenv = require('dotenv');

const port = process.env.PORT || 5000;

const app = require("./app");
dotenv.config({ path: './.env' });

mongoose
.connect(process.env.DATABASE_MONGODB)
.then(() => {
    console.log('Connected to DB successfully');
});

const server = app.listen(port, () => {
    console.log(`Product service is running on port ${port}...`);
});

// SOCKET
const socketIO = require('socket.io')(server, {cors:{origin: '*'}});
exports.onChangeStation = function(data){
    socketIO.emit("status", data);
  };

module.exports = socketIO;
