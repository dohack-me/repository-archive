select User {
    id, username
}
filter .username = <str>$username 
and .password = ext::pgcrypto::crypt(<str>$password, .password)
