mkdir ~p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enabLeCORS = false\n\
headlines = true\n\
\n\
" > ~/.streamlit/config.toml