from F1_lap_time_telementary import get_session_data

year = 2025
grand_prix = 'Chinese Grand Prix'
session_type='Q'
session = get_session_data(year, grand_prix, session_type)

print(session)