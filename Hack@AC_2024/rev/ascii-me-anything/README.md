# ASCII Me Anything

## Description

Simple JS deobfuscation and reverse engineering.

## Intended exploit path

- Identify that the code is obsfuscated JS and put it in a deobfuscator
- Read deobfuscated code and create a function to reverse the encoding function
- Reverse the output of the function to get the input.

```js
// reversed script

function yes(flag) {
  const first = Array.from(flag).map(char => {
    return String.fromCharCode(char.charCodeAt(0) ^ 66);
  }).join("");
  const second = Array.from(first).map(char => {
    return String.fromCharCode(char.charCodeAt(0) + 66);
  }).join("");
  return second;
}
const possibly = yes(flag);
console.log(possibly);

// solve

const fs = require('fs');
const filePath = 'output.txt';
fs.readFile(filePath, (err, data) => {
  const fileBytes = [...data]; 
  console.log('Bytes read: ', fileBytes);
  const reversed_second = fileBytes.map(char => {
    return String.fromCharCode(char - 66);
  }).join("");
  const reversed_first = Array.from(reversed_second).map(char => {
    return String.fromCharCode(char.charCodeAt(0) ^ 66);
  }).join("");
  console.log(reversed_first);
});
```
