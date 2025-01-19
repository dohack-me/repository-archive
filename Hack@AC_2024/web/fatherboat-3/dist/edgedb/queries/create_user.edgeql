insert User {
    username := <str>$username,
    password := ext::pgcrypto::crypt(<str>$password, ext::pgcrypto::gen_salt())
}
