import logging
import requests
import pyodbc
import pandas as pd
import sys
import traceback
import pytz
from dateutil import parser

def get_token(auth_server_url: str, client_id: str, secret: str):
    try:
        token_req = {'client_id': client_id,
                     'client_secret': secret,
                     'grant_type': 'client_credentials'}

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            token_response = requests.post(auth_server_url, data=token_req, headers=headers)
            token_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(traceback.format_exc())
            sys.exit(1)

        tokens = token_response.json()
        return tokens.get('access_token')
    except Exception as e:
        print(traceback.format_exc())


def migrate(api_url: str, schema: str, table_name: str, token: str, conn_string: str, *date_field: str):
    try:
        api_call_headers = {'Authorization': f'Bearer {token}'}
        page = 1

        try:
            conn = pyodbc.connect(conn_string)
            cursor = conn.cursor()
        except Exception as e:
            print(traceback.format_exc())
            sys.exit(1)

        try:
            cursor.execute(f'TRUNCATE TABLE [{schema}].[{table_name}]')
            while True:
                params = {
                    'pageSize': 10000,
                    'page': page
                }
                try:
                    api_call_response = requests.get(api_url, headers=api_call_headers, params=params)
                except Exception as e:
                    print(traceback.format_exc())
                    sys.exit(1)

                if api_call_response.status_code != 200:
                    logging.error(f'Return code: {api_call_response.status_code}. Exiting script.')
                    sys.exit(1)

                response_data = api_call_response.json()
                if 'DataSet' not in response_data:
                    logging.error('No data in response.')
                    sys.exit(1)

                temp_df = pd.DataFrame(response_data['DataSet'])
                rows, _ = temp_df.shape

                if temp_df.empty:
                    break

                col_list = list(temp_df)
                column_names = ','.join(col_list)
                values = '?' * len(col_list)
                values = ','.join(values)

                # Normalize datetime fields to NZST
                nz_tz = pytz.timezone('Pacific/Auckland')

                def normalize_to_nzst(date_str):
                    try:
                        dt = parser.parse(str(date_str))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=pytz.UTC)
                        dt_nzst = dt.astimezone(nz_tz)
                        return dt_nzst.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    except Exception:
                        return None

                for field in date_field:
                    try:
                        temp_df[field] = temp_df[field].apply(normalize_to_nzst)
                    except Exception as e:
                        print(traceback.format_exc())

                try:
                    cursor.fast_executemany = True
                    cursor.executemany(f'INSERT INTO [{schema}].{table_name}'
                                       f'VALUES({values})',
                                       temp_df.values.tolist())
                except Exception as e:
                    print(traceback.format_exc())

                conn.commit()
                page += 1

            logging.info('Closing connection to db')
            conn.close()

        except Exception as e:
            print(traceback.format_exc())

    except Exception as e:
        print(traceback.format_exc())

