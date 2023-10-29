## UI Placeholder
import matplotlib.pyplot as plt
from constants import *
from pathlib import Path


class UIEngine:
    def __init__(self, grid_width=5, world=None) -> None:
        self.grid_size = (grid_width, grid_width)
        self.world = world
        self.step_number = 0
        plt.figure()
        # plt.axis([0, 0, 0, 10])
        plt.ion()

    # [x1,x2] -> [y1,y2]
    def plot_box(
        self,
        x,
        y,
        w,
        text="",
        set_left_wall=False,
        set_right_wall=False,
        set_top_wall=False,
        set_bottom_wall=False,
        color="silver",
    ):
        """
        Plot a box with configurable walls

        Parameters
        ----------
        x : int
            x position of the box
        y : int
            y position of the box
        w : int
            width of the box
        text : str
            text to display in the box
        set_left_wall : bool
            set left wall
        set_right_wall : bool
            set right wall
        set_top_wall : bool
            set top wall
        set_bottom_wall : bool
            set bottom wall
        color : str
            color of the wall
        """
        # left wall
        plt.plot([x, x], [y, y + w], "-", lw=2, color="red" if set_left_wall else color)
        # top wall
        plt.plot(
            [x + w, x],
            [y + w, y + w],
            "-",
            lw=2,
            color="red" if set_top_wall else color,
        )
        # right wall
        plt.plot(
            [x + w, x + w],
            [y, y + w],
            "-",
            lw=2,
            color="red" if set_right_wall else color,
        )
        # bottom wall
        plt.plot(
            [x, x + w], [y, y], "-", lw=2, color="red" if set_bottom_wall else color
        )
        if len(text) > 0:
            color = "black"
            if text == PLAYER_1_NAME:
                color = PLAYER_1_COLOR
            elif text == PLAYER_2_NAME:
                color = PLAYER_2_COLOR
            plt.text(
                x + w / 2,
                y + w / 2,
                text,
                ha="center",
                va="center",
                color="white",
                bbox=dict(facecolor=color, edgecolor=color, boxstyle="round"),
            )

    def plot_grid(self):
        """
        Plot the grid of the game
        """
        for x in range(1, self.grid_size[0] * 2 + 1, 2):
            for y in range(1, self.grid_size[1] * 2 + 1, 2):
                self.plot_box(x, y, 2)

    def plot_game_boundary(
        self,
    ):
        """
        Plot the boundary of the game
        """
        # start y=3 as the y in the range ends in 3
        self.plot_box(1, 3, self.grid_size[0] + self.grid_size[1], color="black")

    def plot_grid_with_board(
        self, chess_board, player_1_pos=None, player_2_pos=None, debug=False
    ):
        """
        Main function to plot the grid of the game

        Parameters
        ----------
        chess_board : np.array of size (grid_size[0], grid_size[1], 4)
            chess board
        player_1_pos : tuple of int
            position of player 1
        player_2_pos : tuple of int
            position of player 2
        debug : bool
            if True, plot the position of the players
        """
        x_pos = 0
        for y in range(self.grid_size[1] * 2 + 1, 1, -2):
            y_pos = 0
            for x in range(1, self.grid_size[0] * 2 + 1, 2):
                up_wall = chess_board[x_pos, y_pos, 0]
                right_wall = chess_board[x_pos, y_pos, 1]
                down_wall = chess_board[x_pos, y_pos, 2]
                left_wall = chess_board[x_pos, y_pos, 3]

                # Display text
                text = ""
                if player_1_pos is not None:
                    if player_1_pos[0] == x_pos and player_1_pos[1] == y_pos:
                        text += "A"
                if player_2_pos is not None:
                    if player_2_pos[0] == x_pos and player_2_pos[1] == y_pos:
                        text += "B"

                if debug:
                    text += " " + str(x_pos) + "," + str(y_pos)

                self.plot_box(
                    x,
                    y,
                    2,
                    set_left_wall=left_wall,
                    set_right_wall=right_wall,
                    set_top_wall=up_wall,
                    set_bottom_wall=down_wall,
                    text=text,
                )
                y_pos += 1
            x_pos += 1

    def fix_axis(self):
        """
        Fix the axis of the plot and set labels
        """
        # Set X labels
        ticks = list(range(0, self.grid_size[0] * 2))
        labels = [x // 2 for x in ticks]
        ticks = [x + 2 for i, x in enumerate(ticks) if i % 2 == 0]
        labels = [x for i, x in enumerate(labels) if i % 2 == 0]
        plt.xticks(ticks, labels)
        # Set Y labels
        ticks = list(range(0, self.grid_size[1] * 2))
        labels = [x // 2 for x in ticks]
        ticks = [x + 3 for i, x in enumerate(ticks) if i % 2 == 1]
        labels = [x for i, x in enumerate(reversed(labels)) if i % 2 == 1]
        plt.yticks(ticks, labels)
        # move x axis to top
        plt.tick_params(bottom=False, labelbottom=False, top=True, labeltop=True)
        plt.xlabel("Y Position")
        plt.ylabel("X Position", position="top")

    def plot_text_info(self):
        """
        Plot game textual information in the bottom
        """
        turn = 1 - self.world.turn
        agent_0 = f"{PLAYER_1_NAME}: {self.world.p0}"
        agent_1 = f"{PLAYER_2_NAME}: {self.world.p1}"
        plt.figtext(
            0.15,
            0.1,
            agent_0,
            wrap=True,
            horizontalalignment="left",
            color=PLAYER_1_COLOR,
            fontweight="bold" if turn == 0 else "normal",
        )
        plt.figtext(
            0.15,
            0.05,
            agent_1,
            wrap=True,
            horizontalalignment="left",
            color=PLAYER_2_COLOR,
            fontweight="bold" if turn == 1 else "normal",
        )

        if len(self.world.results_cache) > 0:
            plt.figtext(
                0.4,
                0.1,
                f"Scores: A: [{self.world.results_cache[1]}], B: [{self.world.results_cache[2]}]",
                horizontalalignment="left",
            )
            if self.world.results_cache[0]:
                # Handle Tie condition
                if self.world.results_cache[1] > self.world.results_cache[2]:
                    win_player = "Player A wins!"
                elif self.world.results_cache[1] < self.world.results_cache[2]:
                    win_player = "Player B wins!"
                else:
                    win_player = "It is a Tie!"

                plt.figtext(
                    0.4,
                    0.05,
                    win_player,
                    horizontalalignment="left",
                    fontweight="bold",
                    color="green",
                )

        plt.figtext(
            0.7, 0.1, f"Max steps: {self.world.max_step}", horizontalalignment="left"
        )

    def render(self, chess_board, p1_pos, p2_pos, debug=False):
        """
        Render the board along with player positions

        Parameters
        ----------
        chess_board : np.array of size (grid_size[0], grid_size[1], 4)
            3D array of pieces
        p1_pos : tuple of int
            position of player 1
        p2_pos : tuple of int
            position of player 2
        debug : bool
            if True, display the position of each piece

        """
        plt.clf()
        self.plot_grid_with_board(chess_board, p1_pos, p2_pos, debug=debug)
        self.plot_game_boundary()
        self.fix_axis()
        self.plot_text_info()
        plt.subplots_adjust(bottom=0.2)
        plt.pause(0.1)
        if self.world.display_save:
            Path(self.world.display_save_path).mkdir(parents=True, exist_ok=True)
            plt.savefig(
                f"{self.world.display_save_path}/{self.world.player_1_name}_{self.world.player_2_name}_{self.step_number}.pdf"
            )
        self.step_number += 1


if __name__ == "__main__":
    engine = UIEngine((5, 5))
    engine.render()
    plt.show()
