import sys
import time
import uuid
from psycopg2 import extras
import psycopg2
from psycopg2 import OperationalError
import xml.etree.ElementTree as ET

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 120


def get_players(root):
    players = [{
        'name': player.find("name").text,
        'country': player.find("country").text,
        'age': float(player.find("age").text),
        'height': float(player.find("height").text),
        'weight': float(player.find("weight").text),
        'draft_year': str(player.find("draft_year").text),
        'draft_round': str(player.find("draft_round").text),
        'draft_number': str(player.find("draft_number").text),
        'season': player.find("season").text,
        'college': {
            'name': player.find("College/name").text,
        },
        'stats': {
            'gp': float(player.find("Stats/gp").text),
            'pts': float(player.find("Stats/pts").text),
            'reb': float(player.find("Stats/reb").text),
            'ast': float(player.find("Stats/ast").text),
            'net_rating': float(player.find("Stats/net_rating").text),
            'oreb_pct': float(player.find("Stats/oreb_pct").text),
            'dreb_pct': float(player.find("Stats/dreb_pct").text),
            'usg_pct': float(player.find("Stats/usg_pct").text),
            'ts_pct': float(player.find("Stats/ts_pct").text),
            'ast_pct': float(player.find("Stats/ast_pct").text),
        }
    } for player in root.findall(".//Player")]

    return players


def check_updates(cursor, last_check):
    query = f"SELECT * FROM imported_documents WHERE updated_on > %s OR created_on > %s;"
    cursor.execute(query, (last_check, last_check))
    data = cursor.fetchall()
    if data:
        return data
    else:
        return None


def check_college_on_db(college):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        query = '''SELECT count(*) from colleges where name=%s'''
        cursor.execute(query, (college,))
        results = cursor.fetchall()
        return results
    except OperationalError as error:
        return print_psycopg2_exception(error)


def insert_college(college):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        college_exists = check_college_on_db(college)
        if college_exists != 0 :
            query = '''INSERT INTO public.colleges(name) VALUES(%s) '''
            cursor.execute(query, (college,))
            connection.commit()
            return "College added successfully."
        else:
            return "College already exists."
    except (Exception, psycopg2.Error) as error:
        print_psycopg2_exception(error)
        return "Error inserting colleges."


def select_college_id(player_college):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        query = '''SELECT id from colleges where name=%s'''
        cursor.execute(query, (player_college,))
        results = cursor.fetchall()
        return results[0][0]
    except OperationalError as error:
        return print_psycopg2_exception(error)


def insert_player(player):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        exists = int(check_player_exists(player['name']))
        college_id = select_college_id(player['college']['name'])
        if exists == 0:
            if player['draft_year'] == 'Undrafted':
                query = '''INSERT INTO public.players(name, country, height, weight, college_id, draft_year, draft_round, draft_number) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) '''
                cursor.execute(query, (
                player['name'], player['country'], player['height'], player['weight'], college_id, 'Undrafted', 'Undrafted',
                'Undrafted'))
                connection.commit()
                return "College added successfully."
            else:
                query = '''INSERT INTO public.players(name, country, height, weight, college_id, draft_year, draft_round, draft_number) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) '''
                cursor.execute(query, (
                player['name'], player['country'], player['height'], player['weight'], college_id, player['draft_year'],
                player['draft_round'], player['draft_number']))
                connection.commit()
                return "Player added successfully."
        else:
            pass
    except (Exception, psycopg2.Error) as error:
        print_psycopg2_exception(error)
        return "Error inserting player."


def select_season_player_id(player):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        query = '''SELECT id FROM season_player WHERE season_id=%s and player_id=%s'''
        query_player_id = '''SELECT id FROM players WHERE name=%s'''
        query_season_id = '''SELECT id FROM seasons WHERE year=%s'''
        cursor.execute(query_player_id, (player['name'],))
        player_id = cursor.fetchone()
        cursor.execute(query_season_id, (player['season'],))
        season_id = cursor.fetchone()
        cursor.execute(query, (season_id, player_id,))
        season_player_id = cursor.fetchone()
        return season_player_id
    except (Exception, psycopg2.Error) as error:
        print_psycopg2_exception(error)
        return "Error counting seasons"


def insert_stats(player, spid):
    global connection, cursor
    print(spid)
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        if spid:
            query = '''INSERT INTO public.stats(season_player, gp, pts, reb, ast, net_rating, oreb_pct, dreb_pct, usg_pct, ts_pct, ast_pct) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(
                query,(spid,player['stats']['gp'],player['stats']['pts'],
                    player['stats']['reb'],
                    player['stats']['ast'],
                    player['stats']['net_rating'],
                    player['stats']['oreb_pct'],
                    player['stats']['dreb_pct'],
                    player['stats']['usg_pct'],
                    player['stats']['ts_pct'],
                    player['stats']['ast_pct'],
                )
            )
            connection.commit()
            return "Stats added successfully."
        else:
            pass
    except (Exception, psycopg2.Error) as error:
        print_psycopg2_exception(error)
        return "Error inserting stats."


def insert_season(season):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        exists = int(check_season_exists(season))
        if exists == 0:
            query = '''INSERT INTO public.seasons(year) VALUES(%s) '''
            cursor.execute(query, (season,))
            connection.commit()
            return "Season added successfully."
        else:
            pass
    except (Exception, psycopg2.Error) as error:
        print_psycopg2_exception(error)
        return "Error inserting seasons."


def insert_player_season(player):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        query_player_id = '''SELECT id FROM players WHERE name=%s'''
        query_season_id = '''SELECT id FROM seasons WHERE year=%s'''
        insert_query = '''INSERT INTO season_player(season_id, player_id) VALUES (%s, %s)'''
        exists = select_season_player_id(player)

        if not exists:
            cursor.execute(query_player_id, (player['name'],))
            player_id = cursor.fetchone()
            cursor.execute(query_season_id, (player['season'],))
            season_id = cursor.fetchone()
            cursor.execute(insert_query, (season_id, player_id))
            connection.commit()
        else:
            pass

    except (Exception, psycopg2.Error) as error:
        print_psycopg2_exception(error)
        return "Error counting seasons"


def check_season_exists(season):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        query = '''SELECT COUNT(*) FROM seasons WHERE year=%s'''
        cursor.execute(query, (season,))
        data = cursor.fetchall()
        return data[0][0]
    except (Exception, psycopg2.Error) as error:
        print_psycopg2_exception(error)
        return "Error counting seasons"

def check_player_exists(name):
    global connection, cursor
    try:
        connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = connection.cursor()
        query = '''SELECT COUNT(*) FROM players WHERE name=%s'''
        cursor.execute(query, (name,))
        data = cursor.fetchall()
        return data[0][0]
    except (Exception, psycopg2.Error) as error:
        print_psycopg2_exception(error)
        return "Error counting seasons"


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_org is None or db_dst is None:
            sys.exit("Failed to connect to the database.")

        # !TODO: 1- Execute a SELECT query to check for any changes on the table

        last_check = '2024-01-19 00:00:00'


        # add check to RabbitMQ message
        try:
            with db_org.cursor() as cursor:
                while last_check:
                    results = check_updates(cursor, last_check)
                    if results is not None:
                        unique_colleges = set()
                        for row in results:
                            xml_data = row[2]
                            try:
                                root = ET.fromstring(xml_data)
                                colleges = [college.find("College/name").text for college in root.findall(".//Player")]
                                seasons = [season.get("season") for season in root.findall(".//Season")]
                                players = get_players(root)
                                # !TODO: 2 - Retreive info that will be added in db-rel
                                for name in colleges:
                                    if name is not None:
                                        if name not in unique_colleges:
                                            unique_colleges.add(name)

                                for name in unique_colleges:
                                    insert_college(name)

                                for season in seasons:
                                    insert_season(season)

                                for player in players:
                                    insert_player(player)
                                    insert_player_season(player)
                                    #spid = select_season_player_id(player)
                                    #print(spid[0])
                                    #insert_stats(player, spid[0])

                            except ET.ParseError as e:
                                print("Error parsing XML data:", e)

                        time.sleep(1)

                    else:
                        print('No results.')

                    last_check = time.strftime('%Y-%m-%d %H:%M:%S')
                    time.sleep(POLLING_FREQ)

        except OperationalError as err:
            print_psycopg2_exception(err)

        db_org.close()
        db_dst.close()
