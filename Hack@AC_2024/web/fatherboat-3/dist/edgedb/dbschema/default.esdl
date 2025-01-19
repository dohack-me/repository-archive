using extension edgeql_http;
using extension pgcrypto;

module default {
    global current_user_id: uuid;
    global current_user := (
        select User filter .id = global current_user_id
    );
    global flag_2 := "ju5t_a_numb3r}";

    type User {
        required username: str {
            constraint exclusive;
        };
        required password: str;

        access policy no_edit 
            deny delete, update;

        access policy view_users
            allow select;

        access policy register
            allow insert;
    }

    type Post {
        required title: str;
        required body: bytes;

        required author: User;

        access policy no_edit
            deny delete, update;

        access policy create_with_auth
            allow insert
            using (global current_user ?!= <User>{});

        access policy read_with_auth
            allow select 
            using (global current_user ?= .author);
    }
}
