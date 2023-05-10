mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
STREAMLIT_SERVER_ADDRESS=0.0.0.0\
STREAMLIT_SERVER_PORT=10000
" > ~/.streamlit/config.toml
