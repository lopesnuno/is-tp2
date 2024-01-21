import json

from database import database


def get_highest_scoring_season_by_player(player_name):
    try:
        query = '''
            SELECT season, points
            FROM (
                SELECT
                    unnest(xpath('//Player[@name="{0}"]/season/text()', xml))::text AS season,
                    unnest(xpath('//Player[@name="{0}"]/Stats/pts/text()', xml))::text AS points
                FROM imported_documents
            ) AS player_seasons
            ORDER BY points::float DESC
            LIMIT 1;
        '''.format(player_name)

        results = database.query(query)
        if results:
            data = {
                'Season': results[0][0],
                'Average Points': results[0][1]
            }
            return json.dumps(data, indent=2)
        else:
            return "No results found."

    except Exception as e:
        return f"An error occurred: {e}"


def get_players_with_tripleDoubleSeasons():
    try:
        query = '''
            SELECT
                player_name,
                COUNT(*) AS triple_double_seasons
            FROM (
                SELECT
                    unnest(xpath('//Player[Stats/pts > 10 and Stats/ast > 10 and Stats/reb > 10]/name/text()', xml))::text AS player_name
                FROM imported_documents
            ) AS triple_double_data
            GROUP BY player_name
            ORDER BY triple_double_seasons DESC
        '''

        results = database.query(query)
        if results:
            top_players = [
                {
                    'Player Name': result[0],
                    'Triple-Double Seasons': result[1]
                }
                for result in results
            ]
            return json.dumps(top_players, indent=2)
        else:
            return "No results found."

    except Exception as e:
        return f"An error occurred: {e}"


def get_top5_colleges():
    try:
        query = '''
            SELECT
                college,
                COUNT(*) AS num_players
            FROM (
                SELECT
                    unnest(xpath('//Player/college/text()', xml))::text AS college
                FROM imported_documents
                WHERE xpath_exists('//Player/college/text()', xml)
            ) AS college_data
            WHERE college IS NOT NULL
            GROUP BY college
            ORDER BY num_players DESC
            LIMIT 5 OFFSET 1;
        '''

        results = database.query(query)
        if results:
            data = [{
                'college': result[0],
                'num_players': result[1],
            } for result in results]

            return json.dumps(data, indent=2)
        else:
            return "No results found."

    except Exception as e:
        return f"An error occurred: {e}"



