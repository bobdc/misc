if [ "$2" != "" ]; then     # if a 2nd parameter was passed
    sqliteFilename=$1
    tableName=$2
else
    echo "add SQLite filename and tablename as parameters"
    exit
fi

outfilename=$sqliteFilename-$tableName
echo "Creating $outfilename.tsv..."
# Make the script for SQLite
echo .open $sqliteFilename > tempsqlite.scr
echo .mode tabs  >> tempsqlite.scr
echo .header on  >> tempsqlite.scr
echo .output $outfilename.tsv  >> tempsqlite.scr
echo "select * from $tableName;"  >> tempsqlite.scr
echo .output stdout  >> tempsqlite.scr

sqlite3 < tempsqlite.scr

echo "Creating $outfilename.ttl..."
~/git/misc/sqliterdf/sqlitetsv2turtle.pl $outfilename.tsv > $outfilename.ttl
