# Fatherboat 3.0

Author: samuzora

> Mandatory fatherboat challenge

**Difficulty: Hard**

## Solution

The db is using edgedb in insecure_dev_mode. This together with the edgeql_http extension defined in the schema will allow us to use urlopen to make a query later.

In util.py, there are 3 checks before the url is visited. The first check resolves the hostname to IP to check if it's localhost, the second check applies a regex to validate the url form, and the third check only allows http or https url schemes.

The first part of the flag can be obtained via CVE-2023-24329. Notice that the python version is 3.11.0, which is vulnerable to CVE-2023-24329. By submitting a url like ` file://localhost/app/flag_1.txt`, with the space in front, the scheme will not be parsed correctly in urlparse, while the url will still be valid in urlopen. This also bypasses the localhost check since the hostname will be messed up as well, giving us the first part of the flag.

The second part of the flag requires accessing the EdgeDB instance. We can use the Docker network alias because it matches the IPv6 regex (after wrapping in square brackets). Then we issue a request to `http://[db]:5656/db/edgedb/edgeql?query=select%20global%20%flag_2` (select global flag_2).
