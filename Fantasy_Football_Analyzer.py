
"""
Tim Dwight
Personal Project
Fantasy Football Analyzer
"""

players = []
weekly_data = []


def clear_menu():
    print('\n' * 30)


def save_players():
    with open('players.txt', 'w') as file:
        for player in players:
            file.write(f'{player[0]},{player[1]}\n')


def load_players():
    try:
        with open('players.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')

                if len(data) == 2:
                    players.append(data)

    except FileNotFoundError:
        with open('players.txt', 'w'):
            pass


def save_weekly_stats():
    with open('weekly_stats.txt', 'w') as file:
        for stats in weekly_data:
            file.write(','.join(stats) + '\n')


def load_weekly_stats():
    try:
        with open('weekly_stats.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')

                if len(data) == 38:
                    weekly_data.append(data)

    except FileNotFoundError:
        with open('weekly_stats.txt', 'w'):
            pass


def menu_list():
    user_input = ''

    while user_input != '0':
        print('\nFANTASY FOOTBALL ANALYZER')
        print('1. View Players')
        print('2. Add Player')
        print('3. Remove Player')
        print('4. Enter Weekly Stats')
        print('5. View Weekly Stats')
        print('6. Edit Weekly Stats')
        print('7. Calculate Fantasy Points')
        print('8. Player Rankings')
        print('9. Compare Players')
        print('10. Team Analysis')
        print('11. Season Summary')
        print('0. Exit')

        user_input = input('Select an option: ')

        if user_input == '1':
            view_players()
        elif user_input == '2':
            add_player()
        elif user_input == '3':
            remove_player()
        elif user_input == '4':
            enter_weekly_stats()
        elif user_input == '5':
            view_weekly_stats()
        elif user_input == '6':
            edit_weekly_stats()
        elif user_input == '7':
            fantasy_points()
        elif user_input == '8':
            player_rankings()
        elif user_input == '9':
            compare_players()
        elif user_input == '10':
            team_analysis()
        elif user_input == '11':
            season_summary()
        elif user_input == '0':
            print('Exiting Fantasy Football Analyzer...')
        else:
            print('Invalid option. Try again.')


def view_players():
    print('\nYOUR PLAYERS')

    if len(players) == 0:
        print('No players have been added.')
    else:
        for player in players:
            print(f'{player[0]} - {player[1]}')


def add_player():
    name = input('Enter player name: ')
    position = input('Enter position (QB, RB, WR, TE, K, D/ST): ')
    position = position.upper()

    if position == 'DST':
        position = 'D/ST'

    if position not in ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST']:
        print('Invalid position.')
        return
    
    for player in players:
        if player[0].lower() == name.lower():
            print('Player already exists.')
            return

    players.append([name, position])
    save_players()

    print(f'{name} has been added.')


def remove_player():
    name = input('Enter player name to remove: ')
    found = False

    for player in players:
        if player[0].lower() == name.lower():
            players.remove(player)
            found = True
            break

    if found:
        for stats in weekly_data[:]:
            if stats[0].lower() == name.lower():
                weekly_data.remove(stats)

        save_players()
        save_weekly_stats()
        print('Player removed.')
    else:
        print('Player not found.')


def enter_stat(data, index, prompt):
    data[index] = input(prompt)


def enter_weekly_stats():
    if len(players) == 0:
        print('Add players before entering stats.')
        return

    print('\nYOUR PLAYERS')

    for player in players:
        print(f'{player[0]} - {player[1]}')

    name = input('\nEnter player name: ')
    found = False
    position = ''

    for player in players:
        if player[0].lower() == name.lower():
            name = player[0]
            position = player[1].upper()
            found = True
            break

    if not found:
        print('Player not found.')
        return

    if position == 'D/ST' or position == 'DST':
        position = 'DEF'

    if position not in ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']:
        print('Invalid player position.')
        return

    week = input('Enter week number: ')

    for stats in weekly_data:
        if stats[0] == name and stats[1] == week:
            print('Stats for this player and week already exist.')
            return

    opponent = input('Enter opponent abbreviation: ').upper()

    # Create a 38-field record.
    # Stats that do not apply remain 0.
    data = ['0'] * 38

    data[0] = name
    data[1] = week
    data[2] = opponent

    print(f'\nEntering stats for {name} ({position})')

    if position == 'QB':
        print('\nPASSING')
        enter_stat(data, 3, 'Completions: ')
        enter_stat(data, 4, 'Passing attempts: ')
        enter_stat(data, 5, 'Passing yards: ')
        enter_stat(data, 6, 'Passing touchdowns: ')
        enter_stat(data, 7, 'Passing 2-point conversions: ')
        enter_stat(data, 8, 'Interceptions thrown: ')

        print('\nFUMBLES')
        enter_stat(data, 9, 'Fumbles lost: ')

        print('\nRUSHING')
        enter_stat(data, 10, 'Carries: ')
        enter_stat(data, 11, 'Rushing yards: ')
        enter_stat(data, 12, 'Rushing touchdowns: ')
        enter_stat(data, 13, 'Rushing 2-point conversions: ')

    elif position == 'RB':
        print('\nRUSHING')
        enter_stat(data, 10, 'Carries: ')
        enter_stat(data, 11, 'Rushing yards: ')
        enter_stat(data, 12, 'Rushing touchdowns: ')
        enter_stat(data, 13, 'Rushing 2-point conversions: ')

        print('\nRECEIVING')
        enter_stat(data, 14, 'Receptions: ')
        enter_stat(data, 15, 'Receiving yards: ')
        enter_stat(data, 16, 'Receiving touchdowns: ')
        enter_stat(data, 17, 'Receiving 2-point conversions: ')

        print('\nOTHER')
        enter_stat(data, 9, 'Fumbles lost: ')
        enter_stat(data, 24, 'Kickoff return touchdowns: ')
        enter_stat(data, 25, 'Punt return touchdowns: ')

    elif position == 'WR' or position == 'TE':
        print('\nRECEIVING')
        enter_stat(data, 14, 'Receptions: ')
        enter_stat(data, 15, 'Receiving yards: ')
        enter_stat(data, 16, 'Receiving touchdowns: ')
        enter_stat(data, 17, 'Receiving 2-point conversions: ')

        print('\nRUSHING')
        enter_stat(data, 10, 'Carries: ')
        enter_stat(data, 11, 'Rushing yards: ')
        enter_stat(data, 12, 'Rushing touchdowns: ')
        enter_stat(data, 13, 'Rushing 2-point conversions: ')

        print('\nOTHER')
        enter_stat(data, 9, 'Fumbles lost: ')
        enter_stat(data, 24, 'Kickoff return touchdowns: ')
        enter_stat(data, 25, 'Punt return touchdowns: ')

    elif position == 'K':
        print('\nKICKING')
        enter_stat(data, 18, 'Extra points made: ')
        enter_stat(data, 19, 'Field goals missed: ')
        enter_stat(data, 20, 'Field goals made (0-39 yards): ')
        enter_stat(data, 21, 'Field goals made (40-49 yards): ')
        enter_stat(data, 22, 'Field goals made (50-59 yards): ')
        enter_stat(data, 23, 'Field goals made (60+ yards): ')

    elif position == 'DEF':
        print('\nDEFENSE / SPECIAL TEAMS')
        enter_stat(data, 24, 'Kickoff return touchdowns: ')
        enter_stat(data, 25, 'Punt return touchdowns: ')
        enter_stat(data, 26, 'Interception return touchdowns: ')
        enter_stat(data, 27, 'Fumble return touchdowns: ')
        enter_stat(data, 28, 'Blocked kick return touchdowns: ')
        enter_stat(data, 29, '2-point returns: ')
        enter_stat(data, 30, '1-point safeties: ')
        enter_stat(data, 31, 'Sacks: ')
        enter_stat(data, 32, 'Blocked kicks: ')
        enter_stat(data, 33, 'Interceptions: ')
        enter_stat(data, 34, 'Fumbles recovered: ')
        enter_stat(data, 35, 'Safeties: ')
        enter_stat(data, 36, 'Points allowed: ')
        enter_stat(data, 37, 'Total yards allowed: ')

    weekly_data.append(data)
    save_weekly_stats()

    print('\nWeekly stats saved successfully.')



def edit_weekly_stats():
    if len(weekly_data) == 0:
        print('No weekly stats available to edit.')
        return

    name = input('Enter player name: ').strip()

    found = []

    for stats in weekly_data:
        if stats[0].lower() == name.lower():
            found.append(stats)

    if len(found) == 0:
        print('Player not found.')
        return

    print(f'\nWeekly stats for {name}:')

    for stats in found:
        print(f'Week {stats[1]} vs. {stats[2]}')

    week = input('\nEnter the week you want to edit: ')

    selected = None

    for stats in found:
        if stats[1] == week:
            selected = stats

    if selected is None:
        print('Week not found.')
        return

    stat_names = [
        'Completions',
        'Passing attempts',
        'Passing yards',
        'Passing touchdowns',
        'Passing 2-point conversions',
        'Interceptions thrown',
        'Fumbles lost',
        'Carries',
        'Rushing yards',
        'Rushing touchdowns',
        'Rushing 2-point conversions',
        'Receptions',
        'Receiving yards',
        'Receiving touchdowns',
        'Receiving 2-point conversions',
        'Extra points made',
        'Field goals missed',
        'FG made 0-39 yards',
        'FG made 40-49 yards',
        'FG made 50-59 yards',
        'FG made 60+ yards',
        'Kickoff return touchdowns',
        'Punt return touchdowns',
        'Interception return touchdowns',
        'Fumble return touchdowns',
        'Blocked kick return touchdowns',
        '2-point returns',
        '1-point safeties',
        'Sacks',
        'Blocked kicks',
        'Defensive interceptions',
        'Fumbles recovered',
        'Safeties',
        'Points allowed',
        'Total yards allowed'
    ]

    print('\nWhich statistic would you like to edit?')

    for i in range(len(stat_names)):
        print(f'{i + 1}. {stat_names[i]}')

    choice = input('\nEnter statistic number: ')

    if not choice.isdigit():
        print('Please enter a valid number.')
        return

    choice = int(choice)

    if choice < 1 or choice > len(stat_names):
        print('Invalid statistic number.')
        return

    index = choice + 2

    print(f'\nCurrent {stat_names[choice - 1]}: {selected[index]}')

    new_value = input('Enter the corrected value: ')

    if not new_value.isdigit():
        print('Please enter a valid whole number.')
        return

    selected[index] = new_value

    save_weekly_stats()

    print('\nWeekly statistic updated successfully!')


def view_weekly_stats():
    name = input('Enter player name or ALL: ')
    found = False

    labels = [
        'Completions',
        'Passing attempts',
        'Passing yards',
        'Passing touchdowns',
        'Passing 2-point conversions',
        'Interceptions thrown',
        'Fumbles lost',
        'Carries',
        'Rushing yards',
        'Rushing touchdowns',
        'Rushing 2-point conversions',
        'Receptions',
        'Receiving yards',
        'Receiving touchdowns',
        'Receiving 2-point conversions',
        'Extra points made',
        'Field goals missed',
        'FG made 0-39 yards',
        'FG made 40-49 yards',
        'FG made 50-59 yards',
        'FG made 60+ yards',
        'Kickoff return touchdowns',
        'Punt return touchdowns',
        'Interception return touchdowns',
        'Fumble return touchdowns',
        'Blocked kick return touchdowns',
        '2-point returns',
        '1-point safeties',
        'Sacks',
        'Blocked kicks',
        'Defensive interceptions',
        'Fumbles recovered',
        'Safeties',
        'Points allowed',
        'Total yards allowed'
    ]

    for stats in weekly_data:
        if name.upper() == 'ALL' or stats[0].lower() == name.lower():
            found = True

            print(f'\n{stats[0]} - Week {stats[1]} vs. {stats[2]}')

            for i in range(3, 38):
                print(f'{labels[i - 3]}: {stats[i]}')

            points = calculate_points(stats)
            print(f'Fantasy points: {points:.2f}')

    if not found:
        print('No weekly stats found.')


def get_stat(stats, index):
    if stats[index].strip() == '':
        return 0
    else:
        return int(stats[index])
    

def calculate_points(stats):
    passing_yards = get_stat(stats, 5)
    passing_td = get_stat(stats, 6)
    passing_2pt = get_stat(stats, 7)
    interceptions = get_stat(stats, 8)
    fumbles_lost = get_stat(stats, 9)

    rushing_yards = get_stat(stats, 11)
    rushing_td = get_stat(stats, 12)
    rushing_2pt = get_stat(stats, 13)

    receptions = get_stat(stats, 14)
    receiving_yards = get_stat(stats, 15)
    receiving_td = get_stat(stats, 16)
    receiving_2pt = get_stat(stats, 17)

    pat = get_stat(stats, 18)
    fg_missed = get_stat(stats, 19)
    fg0 = get_stat(stats, 20)
    fg40 = get_stat(stats, 21)
    fg50 = get_stat(stats, 22)
    fg60 = get_stat(stats, 23)

    kickoff_td = get_stat(stats, 24)
    punt_td = get_stat(stats, 25)
    interception_td = get_stat(stats, 26)
    fumble_td = get_stat(stats, 27)
    blocked_return_td = get_stat(stats, 28)
    return_2pt = get_stat(stats, 29)
    safety_1pt = get_stat(stats, 30)

    sacks = get_stat(stats, 31)
    blocked_kicks = get_stat(stats, 32)
    defensive_int = get_stat(stats, 33)
    fumbles_recovered = get_stat(stats, 34)
    safeties = get_stat(stats, 35)

    points_allowed = get_stat(stats, 36)
    yards_allowed = get_stat(stats, 37)

    points = (
        passing_yards * 0.04
        + passing_td * 4
        + passing_2pt * 2
        - interceptions * 2
        - fumbles_lost * 2
        + rushing_yards * 0.1
        + rushing_td * 6
        + rushing_2pt * 2
        + receptions
        + receiving_yards * 0.1
        + receiving_td * 6
        + receiving_2pt * 2
        + pat
        - fg_missed
        + fg0 * 3
        + fg40 * 4
        + fg50 * 5
        + fg60 * 6
        + kickoff_td * 6
        + punt_td * 6
        + interception_td * 6
        + fumble_td * 6
        + blocked_return_td * 6
        + return_2pt * 2
        + safety_1pt
        + sacks
        + blocked_kicks * 2
        + defensive_int * 2
        + fumbles_recovered * 2
        + safeties * 2
    )

    position = ''

    for player in players:
        if player[0] == stats[0]:
            position = player[1].upper()

    if position == 'D/ST' or position == 'DST':

        if points_allowed == 0:
            points += 5
        elif points_allowed <= 6:
            points += 4
        elif points_allowed <= 13:
            points += 3
        elif points_allowed <= 17:
            points += 1
        elif points_allowed <= 27:
            points += 0
        elif points_allowed <= 34:
            points -= 1
        elif points_allowed <= 45:
            points -= 3
        else:
            points -= 5
        
        if yards_allowed > 0:
            if yards_allowed < 100:
                points += 5
            elif yards_allowed <= 199:
                points += 3
            elif yards_allowed <= 299:
                points += 2
            elif yards_allowed <= 349:
                points += 0
            elif yards_allowed <= 399:
                points -= 1
            elif yards_allowed <= 449:
                points -= 3
            elif yards_allowed <= 499:
                points -= 5
            elif yards_allowed <= 549:
                points -= 6
            else:
                points -= 7

    return points


def fantasy_points():
    if len(weekly_data) == 0:
        print('No weekly stats available.')
        return

    print('\nWEEKLY FANTASY POINTS')

    for stats in weekly_data:
        points = calculate_points(stats)

        print(
            f'{stats[0]} - Week {stats[1]}: '
            f'{points:.2f} points'
        )


def player_rankings():
    totals = []

    for player in players:
        total = 0

        for stats in weekly_data:
            if stats[0] == player[0]:
                total += calculate_points(stats)

        totals.append([player[0], total])

    totals.sort(key=lambda item: item[1], reverse=True)

    print('\nPLAYER RANKINGS')

    for i in range(len(totals)):
        print(
            f'{i + 1}. {totals[i][0]} - '
            f'{totals[i][1]:.2f} points'
        )


def compare_players():
    name1 = input('Enter first player: ')
    name2 = input('Enter second player: ')

    total1 = 0
    total2 = 0

    for stats in weekly_data:
        if stats[0].lower() == name1.lower():
            total1 += calculate_points(stats)

        elif stats[0].lower() == name2.lower():
            total2 += calculate_points(stats)

    print(f'\n{name1}: {total1:.2f} points')
    print(f'{name2}: {total2:.2f} points')

    if total1 > total2:
        print(f'{name1} has more fantasy points.')
    elif total2 > total1:
        print(f'{name2} has more fantasy points.')
    else:
        print('Both players have the same points.')


def team_analysis():
    total = 0

    for stats in weekly_data:
        total += calculate_points(stats)

    print('\nTEAM ANALYSIS')
    print(f'Total team points: {total:.2f}')

    if len(weekly_data) > 0:
        average = total / len(weekly_data)
        print(f'Average points per player-week: {average:.2f}')


def season_summary():
    print('\nSEASON SUMMARY')

    if len(weekly_data) == 0:
        print('No weekly stats available.')
        return

    total = 0
    weeks = []

    for stats in weekly_data:
        points = calculate_points(stats)
        total += points

        if stats[1] not in weeks:
            weeks.append(stats[1])

    average = total / len(weekly_data)

    print(f'Total fantasy points: {total:.2f}')
    print(f'Average points per player-week: {average:.2f}')
    print(f'Weeks recorded: {len(weeks)}')


if __name__ == '__main__':
    load_players()
    load_weekly_stats()
    menu_list()
