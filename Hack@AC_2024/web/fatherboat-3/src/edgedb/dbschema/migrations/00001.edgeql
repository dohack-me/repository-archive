CREATE MIGRATION m16rbyxazzdzl3mhy3auztxhmr44o7jo7tdwwumju62o3mvn72ywzq
    ONTO initial
{
  CREATE EXTENSION pgcrypto VERSION '1.3';
  CREATE EXTENSION edgeql_http VERSION '1.0';
  CREATE GLOBAL default::current_user_id -> std::uuid;
  CREATE TYPE default::User {
      CREATE REQUIRED PROPERTY password: std::str;
      CREATE REQUIRED PROPERTY username: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE ACCESS POLICY no_edit
          DENY UPDATE, DELETE ;
      CREATE ACCESS POLICY register
          ALLOW INSERT ;
      CREATE ACCESS POLICY view_users
          ALLOW SELECT ;
  };
  CREATE GLOBAL default::current_user := (SELECT
      default::User
  FILTER
      (.id = GLOBAL default::current_user_id)
  );
  CREATE TYPE default::Post {
      CREATE ACCESS POLICY create_with_auth
          ALLOW INSERT USING ((GLOBAL default::current_user ?!= <default::User>{}));
      CREATE REQUIRED LINK author: default::User;
      CREATE ACCESS POLICY read_with_auth
          ALLOW SELECT USING ((GLOBAL default::current_user ?= .author));
      CREATE ACCESS POLICY no_edit
          DENY UPDATE, DELETE ;
      CREATE REQUIRED PROPERTY body: std::bytes;
      CREATE REQUIRED PROPERTY title: std::str;
  };
  CREATE GLOBAL default::flag_2 := ('ju5t_a_numb3r}');
};
