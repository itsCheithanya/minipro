const express = require("express");
const app = express();
const PORT = 3000;

const users=[{"username":"cheith",id:0},
{"username":"bhuvan",id:1},
{"username":"bharath",id:2}]

app.get("/hello", (req, res) => {
  res.send("Hello this is a fast page");
});


app.get("/users:id", (req, res) => {
   
  const user=users.find((user)=>user.id==req.params.id);
  setTimeout(() => {
    if (!user) {
        res.status(404).send("No user found");
      } else {
        res.json(user);
      }
  }, 2000);

});

app.listen(PORT, () => {
  console.log("Server is up");
});