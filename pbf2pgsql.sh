

#createdb osm_shanghai;
#PGPASSWORD=docker createdb osm_shanghai -h localhost -U postgres
#PGPASSWORD=docker psql -d  osm_shanghai -h localhost -U postgres -c "CREATE EXTENSION postgis;CREATE EXTENSION hstore"
#PGPASSWORD=docker psql -d  osm_shanghai -h localhost -U postgres -f ~/workspace/osm/tools/osmosis-0.48.0/script/pgsnapshot_schema_0.6.sql
#PGPASSWORD=docker psql -d  osm_shanghai -h localhost -U postgres -f ~/workspace/osm/tools/osmosis-0.48.0/script/pgsnapshot_schema_0.6_action.sql
#PGPASSWORD=docker psql -d  osm_shanghai -h localhost -U postgres -f ~/workspace/osm/tools/osmosis-0.48.0/script/pgsnapshot_schema_0.6_bbox.sql
#PGPASSWORD=docker psql -d  osm_shanghai -h localhost -U postgres -f ~/workspace/osm/tools/osmosis-0.48.0/script/pgsnapshot_schema_0.6_linestring.sql
#~/workspace/osm/tools/osmosis-0.48.0/bin/osmosis  --read-pbf /Users/lgwu/code/rtsense/data/final_shanghai-20200114.osm.pbf.osm.pbf --sort  --write-pgsql database=osm_shanghai host=localhost password=docker user=postgres


# Arguments from command line
pbf=$1
db=$2
osmosis=$3

# Variables from environment
db_host=${DB_HOST:-localhost}
db_port=${DB_PORT:-5432}
db_user=${DB_USER:-postgres}
#db_password=${DB_PASSWORD:-postgres}
db_password=${DB_PASSWORD:-docker}
db_name=$db

# Check if pbf exist
if [[ ! -e $pbf ||  ! -f $pbf ]]; then
  echo "Error: pbf {$pbf} is not specified or not exists!"
  exit 1
fi

if [[ -z $db_name ]]; then
  echo "Error: db name is not specified !"
  exit 1
fi

if [[ -z $osmosis ]]; then
  echo "Error: osmosis is not specified !"
  exit 1
fi

db_option="-h $db_host -p $db_port -U $db_user"
export PGPASSWORD=$db_password


dropdb $db_option --if-exists $db_name
createdb $db_option $db_name
psql $db_option -c "CREATE EXTENSION postgis;CREATE EXTENSION hstore" $db_name
psql $db_option -f ${osmosis}/script/pgsnapshot_schema_0.6.sql $db_name
psql $db_option -f ${osmosis}/script/pgsnapshot_schema_0.6_action.sql $db_name
psql $db_option -f ${osmosis}/script/pgsnapshot_schema_0.6_bbox.sql $db_name
psql $db_option -f ${osmosis}/script/pgsnapshot_schema_0.6_linestring.sql $db_name
${osmosis}/bin/osmosis  --read-pbf $pbf --sort  --write-pgsql database=$db_name host=$db_host password=$db_password user=$db_user


