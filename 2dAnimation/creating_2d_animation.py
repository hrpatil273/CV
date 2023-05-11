import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
import pandas as pd


def plot_field():
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 5))

    # Set axis limits
    plt.xlim([-10, 130])
    plt.ylim([-5, 55])

    # Create field rectangle
    field = patches.Rectangle((0, 0), 120, 50, linewidth=2, edgecolor='white', facecolor='green')
    ax.add_patch(field)

    # Create end zones
    endzone1 = patches.Rectangle((0, 0), 10, 50, linewidth=2, edgecolor='white', facecolor='gray')
    endzone2 = patches.Rectangle((110, 0), 10, 50, linewidth=2, edgecolor='white', facecolor='gray')
    ax.add_patch(endzone1)
    ax.add_patch(endzone2)

    # Create yard lines and numbers
    for i in range(10, 100, 10):
        ax.axvline(i + 10, ymin=0.05, ymax=0.95, color='white')
        if i < 60:
            ax.text(i + 10, 2.5, str(i), fontsize=14, color='white', ha='center')
            ax.text(i + 10, 46.5, str(i), fontsize=14, color='white', ha='center')
        elif i > 60:
            ax.text(i + 10, 46.5, str(100 - i), fontsize=14, color='white', ha='center')
            ax.text(i + 10, 2.5, str(100 - i), fontsize=14, color='white', ha='center')
        else:
            ax.axvline(i, ymin=0.05, ymax=0.95, color='white', linewidth=2)
            ax.text(i + 10, 46.5, str(100 - i), fontsize=14, color='white', ha='center')
            ax.text(i + 10, 2.5, str(100 - i), fontsize=14, color='white', ha='center')

    # Create goal lines and hash marks
    ax.axhline(35, xmin=0.15, xmax=0.85, color='white', linewidth=2)
    ax.axhline(35, xmin=0.445, xmax=0.555, color='white', linewidth=2)
    ax.axhline(15, xmin=0.15, xmax=0.85, color='white', linewidth=2)
    ax.axhline(15, xmin=0.445, xmax=0.555, color='white', linewidth=2)

    # Create labels for end zones and midfield
    ax.text(5, 25, 'END ZONE', fontsize=14, color='white', va='center', rotation='vertical')
    ax.text(115, 25, 'END ZONE', fontsize=14, color='white', va='center', rotation='vertical')
    # ax.text(60, 25, '50', fontsize=14, color='white', ha='center', va='center')
    ax.text(60, 53, 'HOME', fontsize=14, color='grey', ha='center', va='center')
    ax.text(60, -3, 'AWAY', fontsize=14, color='grey', ha='center', va='center')

    # Set background color to dark blue
    fig.set_facecolor('#002244')

    return fig, ax


# position ALL, None, particular (CB, FLB, etc)
# jersey ALL, None, player_number
def save_animation(gameplay, position, jersey):

    df = pd.read_csv('train_player_tracking.csv')
    filtered_df = df[df['game_play'] == str(gameplay)]
    # filtered_df['player_loc'] = df['position'] + "-" + df['jersey_number'].astype(str)

    fig, ax = plot_field()

    # Create empty plots for home and away teams
    home_team = ax.plot([], [], 'ro', markersize=12, alpha=0.7)[0]
    away_team = ax.plot([], [], 'bo', markersize=12, alpha=0.7)[0]

    # Create empty text objects for jersey numbers
    home_numbers = [ax.text(0, 0, '', fontsize=7, color='white', ha='center', va='center') for i in range(11)]
    away_numbers = [ax.text(0, 0, '', fontsize=7, color='white', ha='center', va='center') for i in range(11)]

    # Initialize function for animation
    def animate(frame):
        filtered_df_timed_1 = filtered_df[filtered_df['datetime'] == str(frame)]

        home_x = filtered_df_timed_1[filtered_df_timed_1['team'] == 'home']['x_position']
        home_y = filtered_df_timed_1[filtered_df_timed_1['team'] == 'home']['y_position']
        if position is not None:
            home_jerseys = filtered_df_timed_1[filtered_df_timed_1['team'] == 'home']['position']
        elif jersey is not None:
            home_jerseys = filtered_df_timed_1[filtered_df_timed_1['team'] == 'home']['jersey_number']
        else:
            home_jerseys = filtered_df_timed_1[filtered_df_timed_1['team'] == 'home']['jersey_number']

        away_x = filtered_df_timed_1[filtered_df_timed_1['team'] == 'away']['x_position']
        away_y = filtered_df_timed_1[filtered_df_timed_1['team'] == 'away']['y_position']

        if position is not None:
            away_jerseys = filtered_df_timed_1[filtered_df_timed_1['team'] == 'away']['position']
        elif jersey is not None:
            away_jerseys = filtered_df_timed_1[filtered_df_timed_1['team'] == 'away']['jersey_number']
        else:
            away_jerseys = filtered_df_timed_1[filtered_df_timed_1['team'] == 'away']['jersey_number']

        if position == 'All' or jersey == 'All':
            # Update home team plot and jersey numbers
            home_team.set_data(home_x, home_y)
            for i, (x, y, num) in enumerate(zip(home_x, home_y, home_jerseys)):
                home_numbers[i].set_position((x, y))
                home_numbers[i].set_text(num)

            # Update away team plot and jersey numbers
            away_team.set_data(away_x, away_y)
            for i, (x, y, num) in enumerate(zip(away_x, away_y, away_jerseys)):
                away_numbers[i].set_position((x, y))
                away_numbers[i].set_text(num)
        elif position is not None:
            # Update home team plot and jersey numbers
            home_team.set_data(home_x, home_y)
            for i, (x, y, num) in enumerate(zip(home_x, home_y, home_jerseys)):
                home_numbers[i].set_position((x, y))
                if str(num) in position:
                    home_numbers[i].set_text(num)
                else:
                    home_numbers[i].set_text('')

            # Update away team plot and jersey numbers
            away_team.set_data(away_x, away_y)
            for i, (x, y, num) in enumerate(zip(away_x, away_y, away_jerseys)):
                away_numbers[i].set_position((x, y))
                if str(num) in position:
                    away_numbers[i].set_text(num)
                else:
                    away_numbers[i].set_text('')

        elif jersey is not None:
            # Update home team plot and jersey numbers
            home_team.set_data(home_x, home_y)
            for i, (x, y, num) in enumerate(zip(home_x, home_y, home_jerseys)):
                home_numbers[i].set_position((x, y))
                if str(num) in jersey:
                    home_numbers[i].set_text(num)
                else:
                    home_numbers[i].set_text('')

            # Update away team plot and jersey numbers
            away_team.set_data(away_x, away_y)
            for i, (x, y, num) in enumerate(zip(away_x, away_y, away_jerseys)):
                away_numbers[i].set_position((x, y))
                if str(num) in jersey:
                    away_numbers[i].set_text(num)
                else:
                    away_numbers[i].set_text('')
        else:
            home_team.set_data(home_x, home_y)
            for i, (x, y, num) in enumerate(zip(home_x, home_y, home_jerseys)):
                home_numbers[i].set_position((x, y))
                home_numbers[i].set_text(num)

            # Update away team plot and jersey numbers
            away_team.set_data(away_x, away_y)
            for i, (x, y, num) in enumerate(zip(away_x, away_y, away_jerseys)):
                away_numbers[i].set_position((x, y))
                away_numbers[i].set_text(num)

        return [home_team, away_team] + home_numbers + away_numbers

    # Create animation object
    anim = animation.FuncAnimation(fig, animate, frames=filtered_df['datetime'].unique(), interval=60, blit=True)
    # Show plot
    # plt.show()
    # Save animation to file
    anim.save('static/football_animation_' + gameplay + '.gif', writer='pillow')
    return 'football_animation_' + gameplay + '.gif'

# data = pd.read_csv('train_player_tracking.csv')
# game_play = '58173_003606'
# # save_animation(data, game_play, position='All', jersey=None)
# # # save_animation(data, game_play, position=None, jersey='All')
# # # save_animation(data, game_play, position=None, jersey=['29', '23', '48'])
# save_animation(data, game_play, position=['CB', 'WR'], jersey=None)
