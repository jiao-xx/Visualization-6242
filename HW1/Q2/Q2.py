########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = True

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "xjiao34"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = '''
            Create Table movies(
            id INTEGER,
            title TEXT,
            score REAL
        )
        '''
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = '''
            Create Table movie_cast(
            movie_id INTEGER,
            cast_id INTEGER,
            cast_name TEXT,
            birthday TEXT,
            popularity REAL
        )
        '''
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path, newline='') as movies:
            file_reader = csv.reader(movies)
            query = 'INSERT INTO movies VALUES (?, ?, ?);'
            cursor = connection.cursor()
            for row in file_reader:
                cursor.execute(query, row)
            connection.commit()

       ######################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path, newline='') as movies_cast:
            file_reader = csv.reader(movies_cast)
            query = 'INSERT INTO movie_cast VALUES (?, ?, ?, ?, ?);'
            cursor = connection.cursor()
            for row in file_reader:
                cursor.execute(query, row)
            connection.commit()
        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = '''
         Create Table cast_bio(
            cast_id INTEGER,
            cast_name TEXT,
            birthday TEXT,
            -- set default to 0
            popularity REAL DEFAULT 0,

            PRIMARY KEY (cast_id),

            FOREIGN KEY (cast_id)
                    REFERENCES movie_cast (cast_id)
                    -- linked together
                        ON DELETE CASCADE
                        ON UPDATE NO ACTION
        )
        '''
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = '''
        INSERT INTO  cast_bio 
        SELECT DISTINCT cast_id
        , cast_name
        , birthday
        , popularity
        FROM movie_cast
        '''
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = '''
        CREATE INDEX movie_index ON movies (id)
        '''
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = '''
        CREATE INDEX cast_index ON movie_cast (cast_id)
        '''
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = '''
        CREATE INDEX cast_bio_index ON cast_bio (cast_id)
        '''
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = '''
        WITH ScoreStats AS (
            SELECT
                COUNT(*) AS total_count,
                COUNT(*) FILTER (WHERE score BETWEEN 7 AND 20) AS filtered_count
            FROM
                movies
        )
        SELECT
            printf("%.2f", (filtered_count * 100.0) / total_count)
        FROM
            ScoreStats
        '''
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = '''
        SELECT cast_name
        , COUNT(DISTINCT movie_id) AS appearance_count
        FROM movie_cast
        WHERE popularity > 10
        GROUP BY cast_name
        ORDER BY appearance_count DESC
        LIMIT 5
        '''
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = '''
            WITH temp1 AS (
                SELECT 
                    title AS movie_title, 
                    score AS movie_score, 
                    COUNT(DISTINCT cast_id) AS cast_count
                FROM movie_cast
                INNER JOIN movies ON movie_cast.movie_id = movies.id
                GROUP BY movie_title
                ORDER BY movie_score DESC, cast_count, movie_title
            )
            SELECT movie_title, printf("%.2f", movie_score) AS movie_score, cast_count
            FROM temp1
            LIMIT 5;
        '''
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = '''
        WITH FilteredScores AS (
            SELECT
                mc.cast_id,
                mc.cast_name,
                AVG(m.score) AS average_score
            FROM
                movie_cast mc
                INNER JOIN movies m ON mc.movie_id = m.id
            WHERE
                m.score >= 25
            GROUP BY
                mc.cast_id, mc.cast_name
            HAVING
                COUNT(m.id) >= 3 
        )

        SELECT
            fs.cast_id,
            fs.cast_name,
            printf("%.2f", fs.average_score) AS average_score
        FROM
            FilteredScores fs
        ORDER BY
            fs.average_score DESC,
            fs.cast_name
        LIMIT 10;
        '''
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = '''
        CREATE VIEW good_collaboration AS 

        SELECT
            mc1.cast_id AS cast_member_id1,
            mc2.cast_id AS cast_member_id2,

            COUNT(mc1.movie_id) AS movie_count,
            AVG(m.score) AS average_movie_score

        FROM
            movie_cast mc1
            INNER JOIN movie_cast mc2 ON mc1.movie_id = mc2.movie_id
            INNER JOIN movies m ON mc1.movie_id = m.id  

        WHERE
            mc1.cast_id < mc2.cast_id 
            AND mc1.cast_id != mc2.cast_id

        GROUP BY
            mc1.cast_id, mc2.cast_id

        HAVING
            COUNT(mc1.movie_id) >= 2  
            AND AVG(m.score) >= 40;  
        '''
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = '''
        WITH temp1 AS (
            SELECT cast_member_id1 AS cast_id FROM good_collaboration 
            UNION 
            SELECT cast_member_id2 FROM good_collaboration
        ),

        temp2 AS (
            SELECT 
                temp1.cast_id, 
                AVG(g1.average_movie_score) AS collaboration_score
            FROM 
                temp1
                INNER JOIN good_collaboration g1 ON temp1.cast_id = g1.cast_member_id1 
                                                OR temp1.cast_id = g1.cast_member_id2
            GROUP BY temp1.cast_id
        )

        SELECT 
            DISTINCT temp2.cast_id AS cast_id, 
            mc.cast_name, 
            printf("%.2f", collaboration_score) AS collaboration_score
        FROM 
            temp2
            INNER JOIN movie_cast mc ON mc.cast_id = temp2.cast_id
        ORDER BY 
            collaboration_score DESC, 
            cast_name ASC
        LIMIT 5;
        '''
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = '''
        CREATE VIRTUAL TABLE movie_overview USING fts4(id, overview)
        '''
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        with open('data/movie_overview.csv',errors = 'ignore') as csvfile:
            file = csv.reader(csvfile,delimiter = ',')
            for row in file:
                connection.execute("INSERT INTO movie_overview values (?,?)",(row))
        connection.commit() 
        
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = '''
        SELECT COUNT(id) as count_overview 
        FROM movie_overview 
        WHERE overview MATCH 'fight'
        '''
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = '''
        SELECT COUNT(id) as count_overview 
        FROM movie_overview 
        WHERE overview MATCH 'space NEAR/5 program'
        '''
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except Exception as e:
        print("Error in Table Drops")
        print(e)

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except Exception as e:
         print("Error in Part a.i")
         print(e)

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except Exception as e:
        print("Error in part a.ii")
        print(e)

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except Exception as e:
        print("Error in part a.iii")
        print(e)

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except Exception as e:
        print("Error in part b")
        print(e)

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except Exception as e:
        print("Error in part c")
        print(e)

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except Exception as e:
        print("Error in part d")
        print(e)

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part e")
        print(e)

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part f")
        print(e)
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print("\033[32mRow count for good_collaboration view:\033[m", conn.execute("select count(*) from good_collaboration").fetchall()[0][0])
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part g")
        print(e)

    try:   
        print('\033[32m' + "part h: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.i: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hii(conn)))
    except Exception as e:
        print("Error in part h")
        print(e)

    conn.close()
    #################################################################################
    #################################################################################
  
