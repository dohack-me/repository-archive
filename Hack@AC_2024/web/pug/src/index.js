const express = require("express")
const pug = require("./pug.js")
const runtimeWrap = require('pug-runtime/wrap');
const fs = require("fs")

const PORT = 3000

const app = express()

app.get("/", (req, res) => {
  const data = req.query
  const template = fs.readFileSync("./views/index.pug").toString()
  const out = runtimeWrap(pug.compileBody(template, data).body)(data)
  res.send(out)
})

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`)
})
