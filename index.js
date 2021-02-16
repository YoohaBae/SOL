// require
const mysql = require("mysql");
const session = require("express-session");
const fs = require("fs");
const bodyParser = require("body-parser");
const path = require("path");
const express = require("express");
const sync_mysql = require("sync-mysql");
const app = express();
const url = require("url");
const ejs = require('ejs')

const connection = new sync_mysql({
  host: "localhost",
  user: "root",
  password: "",
  database: "sol_database",
});

app.use(
  session({
    secret: "secret",
    resave: true,
    saveUninitialized: true,
  })
);

app.use(express.static('public'));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.get("/", function (request, response) {
  response.sendFile(path.join(__dirname + "/html/Login.html"));
});

// for action
app.post("/Login", function (request, response) {
  var email = request.body.user.email;
  var password = request.body.user.password;
  console.log(request.body.user);
  if (email && password) {
    // check if user exists
    let passengerDB = connection.query(
      "SELECT * FROM passenger WHERE email = ? AND password = ?",
      [email, password]
    );
    if (passengerDB.length > 0) {
      console.log(passengerDB);
      request.session.loggedin = true;
      request.session.email = email;
      response.redirect("/travel");
    } else {
      response.send("Incorrect Username and/or Password!");
    }
    response.end();
  } else {
    response.send("Please enter Username and Password!");
    response.end();
  }
});
app.get("/Travel", function (request, response) {
  if (request.session.loggedin) {
    var email = request.session.email;
    let passengerDB = connection.query(
      "SELECT * FROM passenger WHERE email = ?",
      [email]
    );
    let passengerID = passengerDB[0].passengerID;
    let addedTicketDB = connection.query(
      "SELECT * FROM addedTicket WHERE passengerID = ?",
      [passengerID]
    );
    if (addedTicketDB.length > 0) {
      const data = { title: 'ejs init', message: 'Hello World', addedTicket: addedTicketDB, passenger: passengerDB[0]};
      response.render('TravelWithTicket.ejs', data);
    } else {
      response.sendFile(path.join(__dirname + "/html/Travel.html"));
    }
  } else {
    response.redirect("/");
  }
});

app.get("/About", (request, response) => {
  if (request.session.loggedin) {
    response.sendFile(path.join(__dirname + "/html/Step1.html"));
  } else {
    response.redirect("/");
  }
});

app.get("/About2", (request, response) => {
  if (request.session.loggedin) {
    response.sendFile(path.join(__dirname + "/html/Step2.html"));
  } else {
    response.redirect("/");
  }
});

app.get("/About3", (request, response) => {
  if (request.session.loggedin) {
    response.sendFile(path.join(__dirname + "/html/Step3.html"));
  } else {
    response.redirect("/");
  }
});

app.get("/Luggage", (request, response) => {
    if (request.session.loggedin) {
        var email = request.session.email;
        let passengerDB = connection.query(
          "SELECT * FROM passenger WHERE email = ?",
          [email]
        );
        let passengerID = passengerDB[0].passengerID;
        let addedTicketDB = connection.query(
          "SELECT * FROM addedTicket WHERE passengerID = ?",
          [passengerID]
        );
        if (addedTicketDB.length > 0) {
            let ticketNumber = addedTicketDB[0].ticketNumber;
            let luggageDB = connection.query(
                "SELECT * FROM luggage WHERE ticketNumber = ?",
                [ticketNumber]
            )
            if (luggageDB.length > 0) {
              console.log(luggageDB);
              const data = { title: 'ejs init', message: 'Hello World', addedLuggage: luggageDB};
              response.render('LuggageWithLuggages.ejs', data);
            } else {
              response.sendFile(path.join(__dirname + "/html/Luggage.html"));
            }
        }
        else {
            response.sendFile(path.join(__dirname + "/html/Luggage.html"));
        }
        
      } else {
        response.redirect("/");
      }
});


app.get("/LuggageArrival/:idx", (request, response, next) => {
  if (request.session.loggedin) {
    var idx = request.params.idx;
    console.log("id=" + idx);
    let luggageDB = connection.query(
      "SELECT * FROM luggage WHERE id = ?",
      [idx]
  )
    const data = { title: 'ejs init', message: 'Hello World', addedLuggage: luggageDB[0]};
    response.render('Luggage-Arrival.ejs', data);
    } else {
      response.redirect("/");
    }
});

app.get("/Logout", (request, response) => {
  request.session.loggedin = false;
  request.session.email = null;
  response.redirect("/");
});

app.get("/AddTicket", (request, response) => {
    if (request.session.loggedin) {
        var email = request.session.email;
        let passengerDB = connection.query(
        "SELECT * FROM passenger WHERE email = ?",
        [email]
        );
        const data = { title: 'ejs init', message: 'Hello World', passenger: passengerDB[0]};
        response.render('AddTicket.ejs', data);
      } else {
        response.redirect("/");
      }
  });

app.post("/AddTicketToDB", (request, response) => {
  var ticketNumber = request.body.ticket.ticketNumber;
  var boardingDate = request.body.ticket.boardingDate;
  let passengerDB = connection.query(
    "SELECT * FROM planeticket WHERE ticketNumber = ?",
    [ticketNumber]
    );
  
  console.log(ticketNumber);
  console.log(boardingDate);
  console.log(passengerDB);
  let ticket = passengerDB[0];
  connection.query(
    `INSERT INTO addedticket(flightNumber, departureTime, departureCity, 
      departureAirport, destinationTime, destinationCity, destinationAirport, passengerID, ticketNumber) 
      VALUES('${ticket.flightNumber}','${ticket.departureTime}','${ticket.departureCity}','${ticket.departureAirport}',
      '${ticket.destinationTime}','${ticket.destinationCity}','${ticket.destinationAirport}', '${ticket.passengerID}','${ticket.ticketNumber}')`
  );
  response.redirect("/Travel");
});

app.listen(3000, () => {
  console.log(`3000번 port에 http server를 띄웠습니다.`);
});
