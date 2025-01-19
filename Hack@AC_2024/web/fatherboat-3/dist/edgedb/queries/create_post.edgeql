insert Post {
    title := <str>$title,
    body := <bytes>$body,
    author := (select User filter .id = <uuid>$author_id)
}
