import express from 'express';
import { createServer } from 'node:http';

import { fileURLToPath } from 'node:url';

import { dirname, join } from 'node:path';

import { Server } from 'socket.io';

import sqlite3 from 'sqlite3';

import { open } from 'sqlite';



// Open the database file

const db = await open({

  filename: 'database.db',

  driver: sqlite3.Database

});



// Create the table if it doesn't exist

await db.run(`

  Create table if not exists messages (

  id INTEGER PRIMARY KEY AUTOINCREMENT,

  client_offset TEXT UNIQUE,

  content TEXT

  )

`);



const app = express();

const server = createServer(app);

const io = new Server(server);



const __dirname = dirname(fileURLToPath(import.meta.url));



app.get('/', (req, res) => {

  res.sendFile(join(__dirname, 'index.html'));

});



io.on('connection', (socket) => {

  console.log(`a connected`);



  socket.on('chat message', async (msg, client_offset) => {

    let result;

    try {

      result = await db.run(`INSERT INTO messages (client_offset, content) values(?,?)`,[client_offset,  msg]) 

    }catch (error) {

      console.log(error) ;

    }



    io.emit('chat message', msg, result.lastID);

  });


  socket.on('disconnect', () => {

    console.log(`a disconnected`);

  });



  socket.onAny((eventName, ...args) => {

    console.log(eventName) ;

    console.log(args) ;

  })



});



server.listen(3000, () => {

  console.log('server running at http://localhost:3000');

});