if LC_ALL=C grep -q '[^[:print:][:space:]]' $1; then
    echo "file contains non-ascii characters"
else
    echo "file contains ascii characters only"
fi
