import psycopg2, logging

from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, LongType, TimestampType, ShortType, DateType
from pyspark.sql.functions import Column

def main():

    logging.info("Process start !")

    # establish a connection to the db
    conn = psycopg2.connect(
        host = "172.18.0.2:5432",
        database = "cars",
        user = "admin",
        password = "admin")

    logger.debug("Connection to PostgreSQL database ...")

    # create a cursor out of a connection; a cursor allows you to communicate with Postgres and execute commands
    cur = conn.cursor()
    spark = initialize_Spark()
    df = loadDFWithSchema(spark)
    df_cleaned = clean_drop_data(df)
    create_table(cur)
    insert_query, cars_seq = write_postgresql(df_cleaned)
    cur.execute(insert_query, cars_seq)

    logging.debug("Data inserted into PostgreSQL database !")
    get_insterted_data(cur)
    cur.close()

    logging.debug("Commiting changes to PostgreSQL database ...")
    conn.commit()

    logging.debug("Closing connection ;)")
    conn.close()

    logging.info("Process done !")


def initialize_Spark():

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("Simple etl job") \
        .getOrCreate()

    logging.debug("Session Spark initialized !")

    return spark

def loadDFWithoutSchema(spark):

    df = spark.read.format("csv").option("header", "true").load("../in/autos.csv")

    return df

def loadDFWithSchema(spark):

    schema = StructType([
        StructField("dateCrawled", TimestampType(), True),
        StructField("name", StringType(), True),
        StructField("seller", StringType(), False),
        StructField("offerType", StringType(), True),
        StructField("price", LongType(), True),
        StructField("abtest", StringType(), True),
        StructField("vehicleType", StringType(), True),
        StructField("yearOfRegistration", StringType(), True),
        StructField("gearbox", StringType(), True),
        StructField("powerPS", ShortType(), True),
        StructField("model", StringType(), True),
        StructField("kilometer", LongType(), True),
        StructField("monthOfRegistration", StringType(), True),
        StructField("fuelType", StringType(), True),
        StructField("brand", StringType(), True),
        StructField("notRepairedDamage", StringType(), True),
        StructField("dateCreated", DateType(), True),
        StructField("nrOfPictures", ShortType(), True),
        StructField("postalCode", StringType(), True),
        StructField("lastSeen", TimestampType(), True)
    ])

    df = spark \
        .read \
        .format("csv") \
        .schema(schema)         \
        .option("header", "true") \
        .load("../in/autos.csv")

    logging.debug("Data loaded into PySpark")

    return df

def clean_drop_data(df):

    df_dropped = df.drop("dateCrawled","nrOfPictures","lastSeen")
    df_filtered = df_dropped.where(Column("seller") != "gewerblich")
    df_dropped_seller = df_filtered.drop("seller")
    df_filtered2 = df_dropped_seller.where(Column("offerType") != "Gesuch")
    df_final = df_filtered2.drop("offerType")

    logging.debug("Data transformed")

    return df_final

def create_table(cursor):

    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS cars_table \
    (   name VARCHAR(255) NOT NULL, \
        price integer NOT NULL, \
        abtest VARCHAR(255) NOT NULL, \
        vehicleType VARCHAR(255), \
        yearOfRegistration VARCHAR(4) NOT NULL, \
        gearbox VARCHAR(255), \
        powerPS integer NOT NULL, \
        model VARCHAR(255), \
        kilometer integer, \
        monthOfRegistration VARCHAR(255) NOT NULL, \
        fuelType VARCHAR(255), \
        brand VARCHAR(255) NOT NULL, \
        notRepairedDamage VARCHAR(255), \
        dateCreated DATE NOT NULL, \
        postalCode VARCHAR(255) NOT NULL);")

        logging.debug("Created table in PostgreSQL")
    except:
        logging.debug("Something went wrong when creating the table")


def write_postgresql(df):

    cars_seq = [tuple(x) for x in df.collect()]

    records_list_template = ','.join(['%s'] * len(cars_seq))

    insert_query = "INSERT INTO cars_table (name, price, abtest, vehicleType, yearOfRegistration, gearbox, powerPS, \
                        model, kilometer, monthOfRegistration, fuelType, brand, notRepairedDamage, dateCreated, postalCode \
                           ) VALUES {}".format(records_list_template)

    logging.debug("Inserting data into PostgreSQL...")

    return insert_query, cars_seq

def get_insterted_data(cursor):

    postgreSQL_select_Query = "select brand, model, price from cars_table"

    cursor.execute(postgreSQL_select_Query)

    cars_records = cursor.fetchmany(2)

    logging.debug("Printing 2 rows")
    for row in cars_records:
        print("Brand = ", row[0], )
        print("Model = ", row[1])
        print("Price  = ", row[2], "\n")

# On configure le logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, filemode='w', format=LOG_FORMAT)
formatter = logging.Formatter(LOG_FORMAT)
logger = logging.getLogger('etl-job')

# Les logs seront inscrits dans un fichier
fileHandler = logging.FileHandler("../log/etl-job.log", mode='w')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.info("Logger initialization complete ...")

if __name__ == '__main__':
    main()